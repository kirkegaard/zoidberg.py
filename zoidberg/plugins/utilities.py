class Utilities():

    def __init__(self, bot):
        self.bot = bot

    def load(self, context, plugin):
        self.bot.load_plugin(plugin)
        context.send('Plugin loaded')

    def reload(self, context, plugin):
        self.bot.reload_plugin(plugin)
        context.send('Plugin reloaded')

    def unload(self, context, plugin):
        self.bot.unload_plugin(plugin)
        context.send('Plugin unloaded')


def setup(bot):
    return Utilities(bot)
