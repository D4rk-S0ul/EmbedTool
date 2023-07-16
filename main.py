import dotenv

import core

dotenv.load_dotenv(".env")

if __name__ == "__main__":
    core.EmbedTool().run("EMBED_TOOL_TOKEN")
