import logging
from slack_bolt.async_app import AsyncApp
from slack_bolt.context.async_context import AsyncAck, AsyncSay
from slack_sdk.web.async_client import AsyncWebClient
from rebm_client import ReBMClient

logger = logging.getLogger(__name__)

class SlackBot:
    def __init__(self, app: AsyncApp, rebm_client: ReBMClient, bot_token: str):
        self.app = app
        self.rebm_client = rebm_client
        self.client = AsyncWebClient(token=bot_token)
        self.setup_handlers()

    async def send_channel_message(self, channel_id: str, text: str):
        """Send a public message to the channel"""
        try:
            await self.client.chat_postMessage(channel=channel_id, text=text)
        except Exception as e:
            logger.error(f"Failed to send channel message: {e}")

    def setup_handlers(self):
        self.app.command("/rebm-help")(self.handle_help)
        self.app.command("/rebm-list")(self.handle_list_nodes)
        self.app.command("/rebm-status")(self.handle_node_status)
        self.app.command("/rebm-reserve")(self.handle_reserve_node)
        self.app.command("/rebm-release")(self.handle_release_node)
        self.app.command("/rebm-create")(self.handle_create_node)
        self.app.command("/rebm-delete")(self.handle_delete_node)
        self.app.command("/rebm-cleanup")(self.handle_cleanup)

    async def handle_help(self, ack: AsyncAck, say: AsyncSay, command):
        await ack()
        await say(text="""
*ReBM Bot Commands*
/rebm-list - List all nodes
/rebm-status <node> - Node status
/rebm-reserve <node> [duration] - Reserve node
  Duration formats:
  • Single word: 1w, 2d, 12h, 90m, 24
  • Two words: 1 week, 2 days, 12 hours, 90 minutes
  • Plain number: 24 (assumes hours)
/rebm-release <node> - Release node
/rebm-create <node> [desc] - Create node
/rebm-delete <node> - Delete node
/rebm-cleanup - Clean up expired
""")

    async def handle_list_nodes(self, ack: AsyncAck, say: AsyncSay, command):
        await ack()
        nodes = await self.rebm_client.get_nodes()
        if not nodes:
            await say(text="No nodes found.")
            return
        msg = "*Nodes:*\n"
        for n in nodes:
            if isinstance(n, dict):
                node_name = n.get('node', n.get('name'))
                status = n.get('status', 'unknown')
            else:
                node_name = str(n)
                status = 'unknown'
            if not node_name:
                continue
            msg += f"- `{node_name}` ({status})\n"
        await say(text=msg)

    async def handle_node_status(self, ack: AsyncAck, say: AsyncSay, command):
        await ack()
        node_name = command.get("text", "").strip()
        if not node_name:
            await say(text="Usage: /rebm-status <node>")
            return
        node_response = await self.rebm_client.get_node(node_name)
        if not node_response or node_response.get("error"):
            all_nodes = await self.rebm_client.get_nodes()
            available_names = []
            for n in all_nodes:
                if isinstance(n, dict):
                    name = n.get('node', n.get('name'))
                else:
                    name = str(n)
                if name:
                    available_names.append(name)
            msg = f"❌ Node `{node_name}` not found.\n"
            if available_names:
                msg += f"Available nodes: {', '.join(f'`{name}`' for name in available_names)}"
            else:
                msg += "No nodes are currently available."
            await say(text=msg)
            return
        msg = f"*Node:* {node_name}\n"
        if isinstance(node_response, dict):
            msg += f"Status: {node_response.get('status', 'unknown')}\n"
            if node_response.get("description"):
                msg += f"Description: {node_response['description']}\n"
            if node_response.get("reservation"):
                r = node_response["reservation"]
                user = r.get('user', 'unknown') if isinstance(r, dict) else str(r)
                expires = r.get('expires', 'unknown') if isinstance(r, dict) else ''
                msg += f"Reserved by: {user} (expires: {expires})\n"
        await say(text=msg)

    def parse_duration(self, duration_str):
        """
        Parse duration string into hours.
        Supports formats: 1w, 2d, 12h, 90m, 1 week, 2 days, 12 hours, 90 minutes, 24
        """
        if not duration_str:
            raise ValueError("Duration cannot be empty")
            
        duration_str = duration_str.strip().lower()
        
        # Handle single-word formats with suffixes
        if duration_str.endswith('w'):
            try:
                return int(duration_str[:-1]) * 7 * 24
            except ValueError:
                raise ValueError(f"Invalid week format: '{duration_str}'. Use format like '1w', '2w'")
        if duration_str.endswith('d'):
            try:
                return int(duration_str[:-1]) * 24
            except ValueError:
                raise ValueError(f"Invalid day format: '{duration_str}'. Use format like '1d', '2d'")
        if duration_str.endswith('h'):
            try:
                return int(duration_str[:-1])
            except ValueError:
                raise ValueError(f"Invalid hour format: '{duration_str}'. Use format like '1h', '12h'")
        if duration_str.endswith('m'):
            try:
                minutes = int(duration_str[:-1])
                if minutes <= 0:
                    raise ValueError("Minutes must be positive")
                return max(1, round(minutes / 60))
            except ValueError:
                raise ValueError(f"Invalid minute format: '{duration_str}'. Use format like '30m', '90m'")
        
        # Handle multi-word formats
        words = duration_str.split()
        if len(words) == 2:
            try:
                number = int(words[0])
                if number <= 0:
                    raise ValueError("Duration number must be positive")
                    
                unit = words[1]
                
                if unit in ['week', 'weeks', 'w']:
                    return number * 7 * 24
                elif unit in ['day', 'days', 'd']:
                    return number * 24
                elif unit in ['hour', 'hours', 'h']:
                    return number
                elif unit in ['minute', 'minutes', 'm']:
                    return max(1, round(number / 60))
                else:
                    raise ValueError(f"Unknown time unit: '{unit}'. Use: week(s), day(s), hour(s), minute(s)")
            except ValueError as e:
                if "Unknown time unit" in str(e):
                    raise e
                raise ValueError(f"Invalid number format: '{words[0]}'. Must be a positive integer")
        
        # Handle plain numbers (assume hours)
        if duration_str.isdigit():
            hours = int(duration_str)
            if hours <= 0:
                raise ValueError("Hours must be positive")
            return hours
            
        # If we get here, the format is not recognized
        raise ValueError(
            f"Invalid duration format: '{duration_str}'. "
            "Supported formats:\n"
            "• Single word: 1w, 2d, 12h, 90m, 24\n"
            "• Two words: 1 week, 2 days, 12 hours, 90 minutes\n"
            "• Plain number: 24 (assumes hours)"
        )

    async def handle_reserve_node(self, ack: AsyncAck, say: AsyncSay, command, body=None, client=None):
        await ack()
        args = command.get("text", "").strip().split()
        if not args:
            await say(text="Usage: /rebm-reserve <node> [duration]")
            return
        
        # Get the real user name first
        user = command.get("user_name", "unknown")
        if body and client:
            user_id = body.get("user_id")
            if user_id:
                try:
                    user_info = await client.users_info(user=user_id)
                    real_name = user_info["user"].get("real_name")
                    if real_name:
                        user = real_name
                except Exception as e:
                    logger.warning(f"Could not fetch real name for user {user_id}: {e}")
        
        # Try to find the node name by checking different combinations of arguments
        node_name = None
        duration_args = []
        
        # First try just the first argument as node name
        potential_node = args[0]
        node_response = await self.rebm_client.get_node(potential_node)
        if node_response and not node_response.get("error"):
            node_name = potential_node
            duration_args = args[1:]
        else:
            # If first argument isn't a node, try joining multiple arguments
            for i in range(1, len(args) + 1):
                potential_node = " ".join(args[:i])
                node_response = await self.rebm_client.get_node(potential_node)
                if node_response and not node_response.get("error"):
                    node_name = potential_node
                    duration_args = args[i:]
                    break
        
        # If no valid node found, show error
        if not node_name:
            all_nodes = await self.rebm_client.get_nodes()
            available_names = []
            for n in all_nodes:
                if isinstance(n, dict):
                    name = n.get('node', n.get('name'))
                else:
                    name = str(n)
                if name:
                    available_names.append(name)
            msg = f"❌ Node `{args[0]}` does not exist.\n"
            if available_names:
                msg += f"Available nodes: {', '.join(f'`{name}`' for name in available_names)}"
            else:
                msg += "No nodes are currently available."
            await say(text=msg)
            return
        
        duration = 24
        original_duration_str = None
        if duration_args:
            try:
                duration_str = " ".join(duration_args)
                original_duration_str = duration_str
                duration = self.parse_duration(duration_str)
            except ValueError as e:
                await say(text=f"Duration error: {str(e)}")
                return
            except Exception as e:
                await say(text=f"Unexpected error parsing duration: {str(e)}")
                return
        
        result = await self.rebm_client.reserve_node(node_name, user, duration)
        if result and result.get("error"):
            error_msg = result.get("error", "").lower()
            details = result.get("details")
            if "not found" in error_msg or "404" in str(result.get("status", "")):
                all_nodes = await self.rebm_client.get_nodes()
                available_names = []
                for n in all_nodes:
                    if isinstance(n, dict):
                        name = n.get('node', n.get('name'))
                    else:
                        name = str(n)
                    if name:
                        available_names.append(name)
                msg = f"❌ Node `{node_name}` does not exist.\n"
                if available_names:
                    msg += f"Available nodes: {', '.join(f'`{name}`' for name in available_names)}"
                else:
                    msg += "No nodes are currently available."
                await say(text=msg)
                return
            elif "already reserved" in error_msg:
                await say(text=f"❌ Node `{node_name}` is already reserved.")
                return
            elif details and isinstance(details, dict):
                detail_msg = details.get("message") or details.get("detail") or str(details)
                if "already reserved" in detail_msg.lower():
                    await say(text=f"❌ Node `{node_name}` is already reserved.")
                    return
                elif "not found" in detail_msg.lower():
                    all_nodes = await self.rebm_client.get_nodes()
                    available_names = []
                    for n in all_nodes:
                        if isinstance(n, dict):
                            name = n.get('node', n.get('name'))
                        else:
                            name = str(n)
                        if name:
                            available_names.append(name)
                    msg = f"❌ Node `{node_name}` does not exist.\n"
                    if available_names:
                        msg += f"Available nodes: {', '.join(f'`{name}`' for name in available_names)}"
                    else:
                        msg += "No nodes are currently available."
                    await say(text=msg)
                    return
                else:
                    await say(text=f"❌ Failed to reserve `{node_name}`: {detail_msg}")
                    return
            else:
                await say(text=f"❌ Failed to reserve `{node_name}`: {result.get('error')}")
                return
        elif result:
            # Check if duration was rounded
            if original_duration_str:
                # Parse the original string again to see if it was rounded
                try:
                    original_hours = self.parse_duration(original_duration_str)
                    if original_hours != duration:
                        await say(text=f"🔒 `{node_name}` reserved for {duration}h (rounded to {duration}h from {original_duration_str}) by {user}.")
                    else:
                        await say(text=f"🔒 `{node_name}` reserved for {duration}h by {user}.")
                except:
                    await say(text=f"🔒 `{node_name}` reserved for {duration}h by {user}.")
            else:
                await say(text=f"🔒 `{node_name}` reserved for {duration}h by {user}.")
        else:
            await say(text=f"❌ Failed to reserve `{node_name}`. No response from server.")

    async def handle_release_node(self, ack: AsyncAck, say: AsyncSay, command, body=None, client=None):
        await ack()
        node_name = command.get("text", "").strip()
        if not node_name:
            await say(text="Usage: /rebm-release <node>")
            return
        
        # Get the real user name
        user = command.get("user_name", "unknown")
        if body and client:
            user_id = body.get("user_id")
            if user_id:
                try:
                    user_info = await client.users_info(user=user_id)
                    real_name = user_info["user"].get("real_name")
                    if real_name:
                        user = real_name
                except Exception as e:
                    logger.warning(f"Could not fetch real name for user {user_id}: {e}")
        
        node_response = await self.rebm_client.get_node(node_name)
        if not node_response or node_response.get("error"):
            all_nodes = await self.rebm_client.get_nodes()
            available_names = []
            for n in all_nodes:
                if isinstance(n, dict):
                    name = n.get('node', n.get('name'))
                else:
                    name = str(n)
                if name:
                    available_names.append(name)
            msg = f"❌ Node `{node_name}` not found.\n"
            if available_names:
                msg += f"Available nodes: {', '.join(f'`{name}`' for name in available_names)}"
            else:
                msg += "No nodes are currently available."
            await say(text=msg)
            return
        result = await self.rebm_client.release_node(node_name)
        if result:
            await say(text=f"🔓 `{node_name}` released by {user}.")
        else:
            await say(text=f"❌ Failed to release `{node_name}`. The node may not be reserved or you may not have permission.")

    async def handle_create_node(self, ack: AsyncAck, say: AsyncSay, command, body=None, client=None):
        await ack()
        args = command.get("text", "").strip().split(" ", 1)
        if not args:
            await say(text="Usage: /rebm-create <node> [desc]")
            return
        
        # Get the real user name
        user = command.get("user_name", "unknown")
        if body and client:
            user_id = body.get("user_id")
            if user_id:
                try:
                    user_info = await client.users_info(user=user_id)
                    real_name = user_info["user"].get("real_name")
                    if real_name:
                        user = real_name
                except Exception as e:
                    logger.warning(f"Could not fetch real name for user {user_id}: {e}")
        
        node_name = args[0]
        desc = args[1] if len(args) > 1 else ""
        existing_node_response = await self.rebm_client.get_node(node_name)
        if existing_node_response and not existing_node_response.get("error"):
            await say(text=f"❌ Node `{node_name}` already exists.")
            return
        result = await self.rebm_client.create_node(node_name, desc)
        if result:
            await say(text=f"✅ Created `{node_name}` by {user}.")
        else:
            await say(text=f"❌ Failed to create `{node_name}`.")

    async def handle_delete_node(self, ack: AsyncAck, say: AsyncSay, command, body=None, client=None):
        await ack()
        node_name = command.get("text", "").strip()
        if not node_name:
            await say(text="Usage: /rebm-delete <node>")
            return
        
        # Get the real user name
        user = command.get("user_name", "unknown")
        if body and client:
            user_id = body.get("user_id")
            if user_id:
                try:
                    user_info = await client.users_info(user=user_id)
                    real_name = user_info["user"].get("real_name")
                    if real_name:
                        user = real_name
                except Exception as e:
                    logger.warning(f"Could not fetch real name for user {user_id}: {e}")
        
        node_response = await self.rebm_client.get_node(node_name)
        if not node_response or node_response.get("error"):
            all_nodes = await self.rebm_client.get_nodes()
            available_names = []
            for n in all_nodes:
                if isinstance(n, dict):
                    name = n.get('node', n.get('name'))
                else:
                    name = str(n)
                if name:
                    available_names.append(name)
            msg = f"❌ Node `{node_name}` not found.\n"
            if available_names:
                msg += f"Available nodes: {', '.join(f'`{name}`' for name in available_names)}"
            else:
                msg += "No nodes are currently available."
            await say(text=msg)
            return
        result = await self.rebm_client.delete_node(node_name)
        if result:
            await say(text=f"✅ Deleted `{node_name}` by {user}.")
        else:
            await say(text=f"❌ Failed to delete `{node_name}`. The node may be reserved or you may not have permission.")

    async def handle_cleanup(self, ack: AsyncAck, say: AsyncSay, command):
        await ack()
        result = await self.rebm_client.cleanup_expired()
        if result:
            await say(text="✅ Cleanup complete.")
        else:
            await say(text="❌ Cleanup failed.") 