from discord.ext import commands
import re

class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(help='Calculator. (use !help math for detail)')
    async def math(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"No, {ctx.subcommand_passed} does not belong to simple")

    @math.command(help='Evaluate a mathematical expression. add, subtract, multiplication, and division only')
    async def calc(self, ctx, *, expression: str):
        # Use regular expression to validate the input expression
        if not re.match("^[-+*/0-9 ]+$", expression):
            await ctx.send("Invalid input. Please provide a valid mathematical expression.")
            return

        try:
            # Use eval() to evaluate the expression
            result = eval(expression)
            await ctx.send(result)
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @math.command(help='add n int inputs.')
    async def add(self, ctx, *numbers: int):
        result = sum(numbers)
        await ctx.send(result)

    @math.command(help='subtract n int inputs.')
    async def subtract(self, ctx, *numbers: int):
        result = numbers[0] - sum(numbers[1:])
        await ctx.send(result)

    @math.command(help='multiplication n int inputs.')
    async def multiplication(self, ctx, *numbers: int):
        result = 1
        for num in numbers:
            result *= num
        await ctx.send(result)

    @math.command(help='division n int inputs.')
    async def division(self, ctx, *numbers: int):
        result = numbers[0]
        for num in numbers[1:]:
            result /= num
        await ctx.send(result)

async def setup(bot):
    await bot.add_cog(Calculator(bot))