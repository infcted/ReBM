import boto3
from datetime import datetime, timedelta, timezone
from decimal import Decimal

class DynamoDBNodeStore:
    def __init__(self, table_name, region_name='us-west-1'):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def _isoformat(self, dt):
        return dt.astimezone(timezone.utc).isoformat()

    def _now(self):
        return datetime.now(timezone.utc)

    def _check_expired(self, item):
        if item.get('expires_at'):
            expires_at = datetime.fromisoformat(item['expires_at'])
            if expires_at < self._now():
                # Auto-release
                self.table.update_item(
                    Key={'node': item['node']},
                    UpdateExpression="""
                        SET #s = :s, reserved_by = :u, expires_at = :e, updated_at = :t
                    """,
                    ExpressionAttributeNames={'#s': 'status'},
                    ExpressionAttributeValues={
                        ':s': 'available',
                        ':u': None,
                        ':e': None,
                        ':t': self._isoformat(self._now())
                    }
                )
                # Update the item in memory
                item['status'] = 'available'
                item['reserved_by'] = None
                item['expires_at'] = None
        return item

    def get_node(self, node_name):
        response = self.table.get_item(Key={'node': node_name})
        item = response.get('Item')
        if not item:
            return None
        return self._check_expired(item)

    def list_nodes(self):
        response = self.table.scan()
        items = response.get('Items', [])
        return [self._check_expired(item) for item in items]

    def create_node(self, node_data):
        # Set default values for new nodes
        node_data['status'] = 'available'  # Nodes are unreserved by default
        node_data['reserved_by'] = None
        node_data['expires_at'] = None
        node_data['updated_at'] = self._isoformat(self._now())
        
        self.table.put_item(Item=node_data)
        return {"message": "Node created", "status": "available"}

    def delete_node(self, node_name):
        self.table.delete_item(Key={'node': node_name})
        return {"message": "Node deleted"}

    def reserve_node(self, node_name, user, expires_at_timestamp):
        node = self.get_node(node_name)
        if not node:
            raise Exception("Node does not exist")
        if node['status'] != 'available':
            raise Exception("Node is not available for reservation")

        # Parse the timestamp - expect ISO format string
        try:
            if isinstance(expires_at_timestamp, str):
                # Handle both timezone-aware and timezone-naive ISO strings
                expires_at = datetime.fromisoformat(expires_at_timestamp)
                # If the datetime is timezone-naive, assume it's in UTC
                if expires_at.tzinfo is None:
                    expires_at = expires_at.replace(tzinfo=timezone.utc)
            else:
                expires_at = datetime.fromtimestamp(expires_at_timestamp, tz=timezone.utc)
        except (ValueError, TypeError):
            raise Exception("Invalid timestamp format. Use ISO format string or Unix timestamp")

        # Check if the expiration time is in the future
        if expires_at <= self._now():
            raise Exception("Expiration time must be in the future")

        self.table.update_item(
            Key={'node': node_name},
            UpdateExpression="""
                SET #s = :s, reserved_by = :u, expires_at = :e, updated_at = :t
            """,
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={
                ':s': 'reserved',
                ':u': user,
                ':e': self._isoformat(expires_at),
                ':t': self._isoformat(self._now())
            }
        )
        return {"message": "Node reserved", "expires_at": self._isoformat(expires_at)}

    def release_node(self, node_name):
        node = self.get_node(node_name)
        if not node:
            raise Exception("Node does not exist")

        self.table.update_item(
            Key={'node': node_name},
            UpdateExpression="""
                SET #s = :s, reserved_by = :u, expires_at = :e, updated_at = :t
            """,
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={
                ':s': 'available',
                ':u': None,
                ':e': None,
                ':t': self._isoformat(self._now())
            }
        )
        return {"message": "Node released"}

    def cleanup_expired_nodes(self):
        """Manually trigger cleanup of expired nodes"""
        response = self.table.scan()
        items = response.get('Items', [])
        cleaned_count = 0
        
        for item in items:
            if item.get('expires_at'):
                expires_at = datetime.fromisoformat(item['expires_at'])
                if expires_at < self._now():
                    self.table.update_item(
                        Key={'node': item['node']},
                        UpdateExpression="""
                            SET #s = :s, reserved_by = :u, expires_at = :e, updated_at = :t
                        """,
                        ExpressionAttributeNames={'#s': 'status'},
                        ExpressionAttributeValues={
                            ':s': 'available',
                            ':u': None,
                            ':e': None,
                            ':t': self._isoformat(self._now())
                        }
                    )
                    cleaned_count += 1
        
        return {"message": f"Cleaned up {cleaned_count} expired nodes"}
