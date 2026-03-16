#  export API MODE=true
export EDU_SHARING_USERNAME="<username here>"
export EDU_SHARING_PASSWORD='<password here>'
export EDU_SHARING_BASE_URL="https://repository.staging.openeduhub.net/edu-sharing/"
export Z_API_KEY="<key for using z-api here>"

export CRAWLER="generic_spider"
export GENERIC_CRAWLER_USE_LLM_API="True"
export GENERIC_CRAWLER_LLM_API_KEY="<key for using GWDG LLM API here>"
export GENERIC_CRAWLER_LLM_API_BASE_URL="https://chat-ai.academiccloud.de/v1"
export GENERIC_CRAWLER_LLM_MODEL="meta-llama-3.1-8b-instruct"
export METADATAAPI_API_KEY="<key for external users of metadata API>"

# For local development:
export GENERIC_CRAWLER_DB_PATH="/Users/jason/src/gen-crawler-ui/database/db.sqlite3"
export API_MODE=false
export PLAYWRIGHT_WS_ENDPOINT="ws://localhost:3000"
export PLAYWRIGHT_CDP_ENDPOINT="http://localhost:9222"
export ARGS=""
