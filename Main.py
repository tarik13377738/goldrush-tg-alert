import asyncio
from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport
from telegram import Bot

GOLDRUSH_API_KEY = "cqt_rQPqpxFxr3CbrWP3Qyd9xFX89mRj"
TELEGRAM_BOT_TOKEN = "8315705861:AAHA1lwPx3mKricJTnFNTYPUyWM1xsQrzyQ"
TELEGRAM_CHANNEL = "@habbynewyear"

KEYWORDS = ["PEPE", "WETH", "HABBY", "MYCOIN"]

bot = Bot(token=TELEGRAM_BOT_TOKEN)

query = gql("""
subscription {
  newPairs(chain_name: BASE_MAINNET, protocols: [UNISWAP_V2, UNISWAP_V3]) {
    base_token_metadata {
      contract_name
      ticker_symbol
    }
    tx_hash
    block_signed_at
  }
}
""")

async def main():
    transport = WebsocketsTransport(
        url="wss://stream.goldrush.dev/graphql",
        init_payload={"api_key": GOLDRUSH_API_KEY}
    )
    async with Client(transport=transport, fetch_schema_from_transport=False) as session:
        async for result in session.subscribe(query):
            pair = result["newPairs"]
            name = pair["base_token_metadata"]["contract_name"] or ""
            ticker = pair["base_token_metadata"]["ticker_symbol"] or ""
            print(f"✅ New pair: {name} ({ticker})")

            if any(keyword.upper() in (name + ticker).upper() for keyword in KEYWORDS):
                msg = (
                    f"🚨 New Pair on Base!\n"
                    f"Name: {name}\n"
                    f"Ticker: {ticker}\n"
                    f"Time: {pair['block_signed_at']}\n"
                    f"Tx: https://basescan.org/tx/{pair['tx_hash']}"
                )
                await bot.send_message(chat_id=TELEGRAM_CHANNEL, text=msg)
                print("✅ Alert sent!")

asyncio.run(main())
