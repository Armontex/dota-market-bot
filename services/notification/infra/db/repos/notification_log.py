from common.db import Repository

from services.notification.common.enums import NotificationChannel
from services.notification.bad.base.models import Log
from .mappers import LogMapper


# NOTESTED
class NotificationRepository(Repository):

    async def create_notification(self, channel: NotificationChannel, log: Log) -> None:
        mapper = LogMapper.get_mapper(channel)
        notification_log = mapper(log)

        async with self._session.begin():
            self._session.add(notification_log)

    # async def get_notifications(self, user_id: int):
    #     query = """
    #         SELECT
    #             n.id,
    #             n.title,
    #             n.message,
    #             n.created_at,
    #             n.is_read
    #         FROM notifications n
    #         WHERE n.user_id = :user_id
    #         ORDER BY n.created_at DESC
    #     """
    #     result = await self.session.execute(query, {"user_id": user_id})
    #     return result.fetchall()
