from discord.gateway import DiscordWebSocket, _log


class SimulatedMobileWebSocket(DiscordWebSocket):
    async def identify(self) -> None:
        """Sends the IDENTIFY packet."""
        payload = {
            "op": self.IDENTIFY,
            "d": {
                "token": self.token,
                "properties": {
                    # These properties tell Discord's gateway that we're
                    # connecting from an Android mobile device, which triggers
                    # mobile status. This leverages a bug/quirk in Discord's
                    # status system where it doesn't properly validate the
                    # authenticity of mobile clients.
                    "os": "Discord Android",
                    "browser": "Discord Android",
                    "device": "",
                },
                "compress": True,
                "large_threshold": 250,
            },
        }

        if self.shard_id is not None and self.shard_count is not None:
            payload["d"]["shard"] = [self.shard_id, self.shard_count]

        state = self._connection
        if state._activity is not None or state._status is not None:
            payload["d"]["presence"] = {
                "status": state._status,
                "game": state._activity,
                "since": 0,
                "afk": False,
            }

        if state._intents is not None:
            payload["d"]["intents"] = state._intents.value

        await self.call_hooks(
            "before_identify", self.shard_id, initial=self._initial_identify
        )
        await self.send_as_json(payload)
        _log.debug(f"Shard ID {self.shard_id} has sent the IDENTIFY payload.")
