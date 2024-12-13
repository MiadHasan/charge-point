import asyncio
import logging
import websockets



from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call, call_result
from ocpp.v16.enums import RegistrationStatus, Action, ClearChargingProfileStatus
from ocpp.routing import on


logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Optimus", charge_point_vendor="The Mobility House"
        )

        response = await self.call(request)

        if response.status == RegistrationStatus.accepted:
            print("Connected to central system.")

    @on(Action.ClearChargingProfile)
    async def clear_charging_profile(self, connector_id: int, **kwargs):
        logging.info(
            "Clear charging profile for connector: %d",
            connector_id
        )
        print("hello")
        return call_result.ClearChargingProfilePayload(
            status=ClearChargingProfileStatus.accepted
        )

async def main():
    async with websockets.connect(
        "ws://localhost:9000/CP_1", subprotocols=["ocpp1.6"]
    ) as ws:

        cp = ChargePoint("CP_1", ws)

        await asyncio.gather(cp.start(), cp.send_boot_notification())


if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())