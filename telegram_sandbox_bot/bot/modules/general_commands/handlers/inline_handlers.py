from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

class InlineHandlers:
    @staticmethod
    async def handle_inline_query(client, inline_query):
        results = [
            InlineQueryResultArticle(
                title="Grow your dick",
                input_message_content=InputTextMessageContent("/grow"),
                description="Daily growth command"
            ),
            InlineQueryResultArticle(
                title="Check top",
                input_message_content=InputTextMessageContent("/top"),
                description="Show leaderboard"
            )
        ]
        
        await client.answer_inline_query(
            inline_query.id,
            results=results,
            cache_time=1
        )
