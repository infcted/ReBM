import logging
from slack_bolt.async_app import AsyncApp
from slack_bolt.context.async_context import AsyncAck, AsyncSay
from rebm_client import ReBMClient

logger = logging.getLogger(__name__)

class SlackBot:
    def __init__(self, app: AsyncApp, rebm_client: ReBMClient):
        self.app = app
        self.rebm_client = rebm_client
        self.setup_handlers()

    def setup_handlers(self):
        self.app.command("/rebm-help")(self.handle_help)
        self.app.command("/rebm-list")(self.handle_list_nodes)
        self.app.command("/rebm-status")(self.handle_node_status)
        self.app.command("/rebm-reserve")(self.handle_reserve_node)
        self.app.command("/rebm-release")(self.handle_release_node)
        self.app.command("/rebm-create")(self.handle_create_node)
        self.app.command("/rebm-delete")(self.handle_delete_node)
        self.app.command("/rebm-cleanup")(self.handle_cleanup)

    async def handle_help(self, ack: AsyncAck, say: AsyncSay):
        await ack()
        await say(text="""
*ReBM Bot Commands*
/rebm-list - List all nodes
/rebm-status <node> - Node status
/rebm-reserve <node> [hours] - Reserve node
/rebm-release <node> - Release node
/rebm-create <node> [desc] - Create node
/rebm-delete <node> - Delete node
/rebm-cleanup - Clean up expired
""")

    async def handle_list_nodes(self, ack: AsyncAck, say: AsyncSay):
        await ack()
        nodes = await self.rebm_client.get_nodes()
        if not nodes:
            await say(text="No nodes found.")
            return
        msg = "*Nodes:*\n"
        for n in nodes:
            msg += f"- `{n['name']}` ({n.get('status', 'unknown')})\n"
        await say(text=msg)

    async def handle_node_status(self, ack: AsyncAck, say: AsyncSay, command):
        await ack()
        node_name = command.get("text", "").strip()
        if not node_name:
            await say(text="Usage: /rebm-status <node>")
            return
        node = await self.rebm_client.get_node(node_name)
        if not node:
            await say(text=f"Node `{node_name}` not found.")
            return
        msg = f"*Node:* {node_name}\nStatus: {node.get('status', 'unknown')}\n"
        if node.get("description"):
            msg += f"Description: {node['description']}\n"
        if node.get("reservation"):
            r = node["reservation"]
            msg += f"Reserved by: {r.get('user', 'unknown')} (expires: {r.get('expires', 'unknown')})\n"
        await say(text=msg)

    async def handle_reserve_node(self, ack: AsyncAck, say: AsyncSay, command):
        await ack()
        args = command.get("text", "").strip().split()
        if not args:
            await say(text="Usage: /rebm-reserve <node> [hours]")
            return
        node_name = args[0]
        duration = int(args[1]) if len(args) > 1 and args[1].isdigit() else 24
        user = command.get("user_name", "unknown")
        result = await self.rebm_client.reserve_node(node_name, user, duration)
        if result:
            await say(text=f"Reserved `{node_name}` for {duration}h.")
        else:
            await say(text=f"Failed to reserve `{node_name}`.")

    async def handle_release_node(self, ack: AsyncAck, say: AsyncSay, command):
        await ack()
        node_name = command.get("text", "").strip()
        if not node_name:
            await say(text="Usage: /rebm-release <node>")
            return
        result = await self.rebm_client.release_node(node_name)
        if result:
            await say(text=f"Released `{node_name}`.")
        else:
            await say(text=f"Failed to release `{node_name}`.")

    async def handle_create_node(self, ack: AsyncAck, say: AsyncSay, command):
        await ack()
        args = command.get("text", "").strip().split(" ", 1)
        if not args:
            await say(text="Usage: /rebm-create <node> [desc]")
            return
        node_name = args[0]
        desc = args[1] if len(args) > 1 else ""
        result = await self.rebm_client.create_node(node_name, desc)
        if result:
            await say(text=f"Created `{node_name}`.")
        else:
            await say(text=f"Failed to create `{node_name}`.")

    async def handle_delete_node(self, ack: AsyncAck, say: AsyncSay, command):
        await ack()
        node_name = command.get("text", "").strip()
        if not node_name:
            await say(text="Usage: /rebm-delete <node>")
            return
        result = await self.rebm_client.delete_node(node_name)
        if result:
            await say(text=f"Deleted `{node_name}`.")
        else:
            await say(text=f"Failed to delete `{node_name}`.")

    async def handle_cleanup(self, ack: AsyncAck, say: AsyncSay):
        await ack()
        result = await self.rebm_client.cleanup_expired()
        if result:
            await say(text="Cleanup complete.")
        else:
            await say(text="Cleanup failed.") 