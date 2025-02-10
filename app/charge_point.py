import logging
from ocpp.v16 import ChargePoint as BaseChargePoint
from ocpp.v16 import call, call_result
from ocpp.v16.enums import RegistrationStatus, Action, ClearChargingProfileStatus
from ocpp.routing import on

logging.basicConfig(level=logging.INFO)


class ChargePoint(BaseChargePoint):
    async def send_boot_notification(self):
        """Send Boot Notification to the central system."""
        request = call.BootNotification(
            charge_point_model="Optimus", charge_point_vendor="The Mobility House"
        )
        response = await self.call(request)

        if response.status == RegistrationStatus.accepted:
            logging.info("Connected to central system.")

    @on(Action.ClearChargingProfile)
    def clear_charging_profile(self, connector_id: int, **kwargs):
        """Clear the charging profile for a specific connector."""
        logging.info("Clear charging profile for connector: %d", connector_id)
        return call_result.ClearChargingProfile(
            status=ClearChargingProfileStatus.accepted
        )
