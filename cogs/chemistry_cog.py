import discord
import re
import sympy
from sympy.abc import x
from discord.ext import commands
from sympy import symbols, Eq, solve

class Chemistry(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.report_command_pattern = re.compile(r'^!report_Chemistry\b', re.IGNORECASE)

    @commands.command(
        name='report_Chemistry',
        help='Report apabila ada kesalahan pada reaksi kimia asam - basa',
        description='Report apabila ada kesalahan pada reaksi kimia asam - basa',
    )
    async def report_chemistry_command(self, ctx, *, pesan: str):
        try:
            # Cek jika pemilik server ada
            bot_owner = self.bot.get_user(440514731380441091)
            if bot_owner:
                # Kirim pesan error kepada pemilik bot melalui bot Discord
                await bot_owner.send(f"***Laporan Error di Reaksi Kimia Asam - Basa, dari {ctx.author.name} ({ctx.author.id}) di Server {ctx.guild.name} ({ctx.guild.id}):***\n{pesan}")
            else:
                await ctx.send("***Gagal mengirim laporan kepada pemilik bot.***")
        except Exception as e:
            # Tangani exception jika terjadi kesalahan
            await ctx.send(f"***Terjadi kesalahan saat mengirim laporan:***\n{str(e)}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.report_command_pattern.search(message.content):
            # Reply directly to the user's message
            await message.reply("***Laporan Reaksi Kimia Telah Dikirim kepada Pemilik Bot!***")

    @commands.command(
        name='reaksi-Asam_Basa',
        help='Lakukan reaksi asam-basa dan dapatkan hasilnya.',
        usage='!reaksi-asam_basa [senyawa_asam] [senyawa_basa]',
        description='Melakukan reaksi asam-basa dengan senyawa asam dan basa yang diberikan.\nGunakan !reaksi-asam_basa [senyawa asam] [senyawa_basa] \nContoh: !reaksi-asam_basa H2SO4 NaOH',
    )
    async def reaksi_asam_basa_command(self, ctx, senyawa_asam, senyawa_basa):
        """
        Melakukan reaksi asam-basa dengan senyawa asam dan basa yang diberikan.

        Args:
          senyawa_asam (str): Senyawa asam yang akan direaksikan.
          senyawa_basa (str): Senyawa basa yang akan direaksikan.
        """
        hasil_reaksi = self.reaksi_asam_basa(senyawa_asam, senyawa_basa)
        await ctx.send(f"***Hasil Reaksi Asam-Basa:***\n{hasil_reaksi}")

    def reaksi_asam_basa(self, senyawa_asam, senyawa_basa):
        # Daftar senyawa-senyawa asam kuat
        asam = ['HCl', 'HBr', 'HI', 'H2SO4', 'HNO3', 'HClO4', 'HF', 'HBrO4', 'HIO3', 'HNO2', 'HClO3']

        # Daftar senyawa-senyawa basa kuat
        basa = ['NaOH', 'KOH', 'Ca(OH)2', 'Mg(OH)2', 'Al(OH)3', 'Fe(OH)3', 'NH4OH', 'Mn(OH)2', 'Zn(OH)2', 'Cu(OH)2', 'Fe(OH)2', 'Al(OH)2', 'Na2CO3', 'K2CO3']

        # Tabel senyawa hasil reaksi dari kombinasi asam-basa
        tabel_hasil_reaksi = {
            #NaOH
            ('HCl', 'NaOH'): 'HCl + NaOH -> NaCl + H2O',
            ('HBr', 'NaOH'): 'HBr + NaOH -> NaBr + H2O',
            ('HI', 'NaOH'): 'HI + NaOH -> NaI + H2O',
            ('H2SO4', 'NaOH'): 'H2SO4 + 2NaOH -> Na2SO4 + 2H2O',
            ('HNO3', 'NaOH'): 'HNO3 + NaOH -> NaNO3 + H2O',
            ('HClO4', 'NaOH'): 'HClO4 + NaOH -> NaClO4 + H2O',
            ('HF', 'NaOH'): 'HF + NaOH -> NaF + H2O',
            ('HBrO4', 'NaOH'): 'HBrO4 + NaOH -> NaBrO4 + H2O',
            ('HIO3', 'NaOH'): 'HIO3 + NaOH -> NaIO3 + H2O',
            ('HNO2', 'NaOH'): 'HNO2 + NaOH -> NaNO2 + H2O',
            ('HClO3', 'NaOH'): 'HClO3 + NaOH -> NaClO3 + H2O',
            #KOH
            ('HCl', 'KOH'): 'HCl + KOH -> KCl + H2O',
            ('HBr', 'KOH'): 'HBr + KOH -> KBr + H2O',
            ('HI', 'KOH'): 'HI + KOH -> KI + H2O',
            ('H2SO4', 'KOH'): 'H2SO4 + 2KOH -> K2SO4 + 2H2O',
            ('HNO3', 'KOH'): 'HNO3 + KOH -> KNO3 + H2O',
            ('HClO4', 'KOH'): 'HClO4 + KOH -> KClO4 + H2O',
            ('HF', 'KOH'): 'HF + KOH -> KF + H2O',
            ('HBrO4', 'KOH'): 'HBrO4 + KOH -> KBrO4 + H2O',
            ('HIO3', 'KOH'): 'HIO3 + KOH -> KIO3 + H2O',
            ('HNO2', 'KOH'): 'HNO2 + KOH -> KNO2 + H2O',
            ('HClO3', 'KOH'): 'HClO3 + KOH -> KClO3 + H2O',
            #Ca(OH)2
            ('HCl', 'Ca(OH)2'): '2HCl + Ca(OH)2 -> CaCl2 + 2H2O',
            ('HBr', 'Ca(OH)2'): '2HBr + Ca(OH)2 -> CaBr2 + 2H2O',
            ('HI', 'Ca(OH)2'): '2HI + Ca(OH)2 -> CaI2 + 2H2O',
            ('H2SO4', 'Ca(OH)2'): 'H2SO4 + Ca(OH)2 -> CaSO4 + 2H2O',
            ('HNO3', 'Ca(OH)2'): '2HNO3 + Ca(OH)2 -> Ca(NO3)2 + 2H2O',
            ('HClO4', 'Ca(OH)2'): '2HClO4 + Ca(OH)2 -> Ca(ClO4)2 + 2H2O',
            ('HF', 'Ca(OH)2'): '2HF + Ca(OH)2 -> CaF2 + 2H2O',
            ('HBrO4', 'Ca(OH)2'): '2HBrO4 + Ca(OH)2 -> Ca(BrO4)2 + 2H2O',
            ('HIO3', 'Ca(OH)2'): '2HIO3 + Ca(OH)2 -> Ca(IO3)2 + 2H2O',
            ('HNO2', 'Ca(OH)2'): '2HNO2 + Ca(OH)2 -> Ca(NO2)2 + 2H2O',
            ('HClO3', 'Ca(OH)2'): '2HClO3 + Ca(OH)2 -> Ca(ClO3)2 + 2H2O',
            #Mg(OH)2
            ('HCl', 'Mg(OH)2'): '2HCl + Mg(OH)2 -> MgCl2 + 2H2O',
            ('HBr', 'Mg(OH)2'): '2HBr + Mg(OH)2 -> MgBr2 + 2H2O',
            ('HI', 'Mg(OH)2'): '2HI + Mg(OH)2 -> MgI2 + 2H2O',
            ('H2SO4', 'Mg(OH)2'): 'H2SO4 + Mg(OH)2 -> MgSO4 + 2H2O',
            ('HNO3', 'Mg(OH)2'): '2HNO3 + Mg(OH)2 -> Mg(NO3)2 + 2H2O',
            ('HClO4', 'Mg(OH)2'): '2HClO4 + Mg(OH)2 -> Mg(ClO4)2 + 2H2O',
            ('HF', 'Mg(OH)2'): '2HF + Mg(OH)2 -> MgF2 + 2H2O',
            ('HBrO4', 'Mg(OH)2'): '2HBrO4 + Mg(OH)2 -> Mg(BrO4)2 + 2H2O',
            ('HIO3', 'Mg(OH)2'): '2HIO3 + Mg(OH)2 -> Mg(IO3)2 + 2H2O',
            ('HNO2', 'Mg(OH)2'): '2HNO2 + Mg(OH)2 -> Mg(NO2)2 + 2H2O',
            ('HClO3', 'Mg(OH)2'): '2HClO3 + Mg(OH)2 -> Mg(ClO3)2 + 2H2O',
            #Al(OH)3
            ('HCl', 'Al(OH)3'): '3HCl + Al(OH)3 -> AlCl3 + 3H2O',
            ('HBr', 'Al(OH)3'): '3HBr + Al(OH)3 -> AlBr3 + 3H2O',
            ('HI', 'Al(OH)3'): '3HI + Al(OH)3 -> AlI3 + 3H2O',
            ('H2SO4', 'Al(OH)3'): '3H2SO4 + 2Al(OH)3 -> Al2(SO4)3 + 6H2O',
            ('HNO3', 'Al(OH)3'): '3HNO3 + Al(OH)3 -> Al(NO3)3 + 3H2O',
            ('HClO4', 'Al(OH)3'): '3HClO4 + Al(OH)3 -> Al(ClO4)3 + 3H2O',
            ('HF', 'Al(OH)3'): '3HF + Al(OH)3 -> AlF3 + 3H2O',
            ('HBrO4', 'Al(OH)3'): '3HBrO4 + Al(OH)3 -> Al(BrO4)3 + 3H2O',
            ('HIO3', 'Al(OH)3'): '3HIO3 + Al(OH)3 -> Al(IO3)3 + 3H2O',
            ('HNO2', 'Al(OH)3'): '3HNO2 + Al(OH)3 -> Al(NO2)3 + 3H2O',
            ('HClO3', 'Al(OH)3'): '3HClO3 + Al(OH)3 -> Al(ClO3)3 + 3H2O',
            #Fe(OH)3
            ('HCl', 'Fe(OH)3'): '6HCl + 2Fe(OH)3 -> 2FeCl3 + 6H2O',
            ('HBr', 'Fe(OH)3'): '6HBr + 2Fe(OH)3 -> 2FeBr3 + 6H2O',
            ('HI', 'Fe(OH)3'): '6HI + 2Fe(OH)3 -> 2FeI3 + 6H2O',
            ('H2SO4', 'Fe(OH)3'): '3H2SO4 + 2Fe(OH)3 -> Fe2(SO4)3 + 6H2O',
            ('HNO3', 'Fe(OH)3'): '6HNO3 + 2Fe(OH)3 -> 2Fe(NO3)3 + 6H2O',
            ('HClO4', 'Fe(OH)3'): '6HClO4 + 2Fe(OH)3 -> 2Fe(ClO4)3 + 6H2O',
            ('HF', 'Fe(OH)3'): '6HF + 2Fe(OH)3 -> 2FeF3 + 6H2O',
            ('HBrO4', 'Fe(OH)3'): '6HBrO4 + 2Fe(OH)3 -> 2Fe(BrO4)3 + 6H2O',
            ('HIO3', 'Fe(OH)3'): '6HIO3 + 2Fe(OH)3 -> 2Fe(IO3)3 + 6H2O',
            ('HNO2', 'Fe(OH)3'): '6HNO2 + 2Fe(OH)3 -> 2Fe(NO2)3 + 6H2O',
            ('HClO3', 'Fe(OH)3'): '6HClO3 + 2Fe(OH)3 -> 2Fe(ClO3)3 + 6H2O',
            #NH4OH
            ('HCl', 'NH4OH'): 'HCl + NH4OH -> H2O + NH4Cl',
            ('HBr', 'NH4OH'): 'HBr + NH4OH -> H2O + NH4Br',
            ('HI', 'NH4OH'): 'HI + NH4OH -> H2O + NH4I',
            ('H2SO4', 'NH4OH'): 'H2SO4 + 2NH4OH -> 2H2O + (NH4)2SO4',
            ('HNO3', 'NH4OH'): 'HNO3 + NH4OH -> H2O + NH4NO3',
            ('HClO4', 'NH4OH'): 'HClO4 + NH4OH -> H2O + NH4ClO4',
            ('HF', 'NH4OH'): 'HF + NH4OH -> H2O + NH4F',
            ('HBrO4', 'NH4OH'): 'HBrO4 + NH4OH -> H2O + NH4BrO4',
            ('HIO3', 'NH4OH'): 'HIO3 + NH4OH -> H2O + NH4IO3',
            ('HNO2', 'NH4OH'): 'HNO2 + NH4OH -> H2O + NH4NO2',
            ('HClO3', 'NH4OH'): 'HClO3 + NH4OH -> H2O + NH4ClO3',
            #Mn(OH)2
            ('HCl', 'Mn(OH)2'): '2HCl + Mn(OH)2 -> 2H2O + MnCl2',
            ('HBr', 'Mn(OH)2'): '2HBr + Mn(OH)2 -> 2H2O + MnBr2',
            ('HI', 'Mn(OH)2'): '2HI + Mn(OH)2 -> 2H2O + MnI2',
            ('H2SO4', 'Mn(OH)2'): 'H2SO4 + Mn(OH)2 -> 2H2O + MnSO4',
            ('HNO3', 'Mn(OH)2'): '2HNO3 + Mn(OH)2 -> 2H2O + Mn(NO3)2',
            ('HClO4', 'Mn(OH)2'): '2HClO4 + Mn(OH)2 -> 2H2O + Mn(ClO4)2',
            ('HF', 'Mn(OH)2'): '2HF + Mn(OH)2 -> 2H2O + MnF2',
            ('HBrO4', 'Mn(OH)2'): '2HBrO4 + Mn(OH)2 -> 2H2O + Mn(BrO4)2',
            ('HIO3', 'Mn(OH)2'): '2HIO3 + Mn(OH)2 -> 2H2O + Mn(IO3)2',
            ('HNO2', 'Mn(OH)2'): '2HNO2 + Mn(OH)2 -> 2H2O + Mn(NO2)2',
            ('HClO3', 'Mn(OH)2'): '2HClO3 + Mn(OH)2 -> 2H2O + Mn(ClO3)2',
            #Zn(OH)2
            ('HCl', 'Zn(OH)2'): '2HCl + Zn(OH)2 -> 2H2O + ZnCl2',
            ('HBr', 'Zn(OH)2'): '2HBr + Zn(OH)2 -> 2H2O + ZnBr2',
            ('HI', 'Zn(OH)2'): '2HI + Zn(OH)2 -> 2H2O + ZnI2',
            ('H2SO4', 'Zn(OH)2'): 'H2SO4 + Zn(OH)2 -> 2H2O + ZnSO4',
            ('HNO3', 'Zn(OH)2'): '2HNO3 + Zn(OH)2 -> 2H2O + Zn(NO3)2',
            ('HClO4', 'Zn(OH)2'): '2HClO4 + Zn(OH)2 -> 2H2O + Zn(ClO4)2',
            ('HF', 'Zn(OH)2'): '2HF + Zn(OH)2 -> 2H2O + ZnF2',
            ('HBrO4', 'Zn(OH)2'): '2HBrO4 + Zn(OH)2 -> 2H2O + Zn(BrO4)2',
            ('HIO3', 'Zn(OH)2'): '2HIO3 + Zn(OH)2 -> 2H2O + Zn(IO3)2',
            ('HNO2', 'Zn(OH)2'): '2HNO2 + Zn(OH)2 -> 2H2O + Zn(NO2)2',
            ('HClO3', 'Zn(OH)2'): '2HClO3 + Zn(OH)2 -> 2H2O + Zn(ClO3)2',
            #Cu(OH)2
            ('HCl', 'Cu(OH)2'): '2HCl + Cu(OH)2 -> 2H2O + CuCl2',
            ('HBr', 'Cu(OH)2'): '2HBr + Cu(OH)2 -> 2H2O + CuBr2',
            ('HI', 'Cu(OH)2'): '2HI + Cu(OH)2 -> 2H2O + CuI2',
            ('H2SO4', 'Cu(OH)2'): 'H2SO4 + Cu(OH)2 -> 2H2O + CuSO4',
            ('HNO3', 'Cu(OH)2'): '2HNO3 + Cu(OH)2 -> 2H2O + Cu(NO3)2',
            ('HClO4', 'Cu(OH)2'): '2HClO4 + Cu(OH)2 -> 2H2O + Cu(ClO4)2',
            ('HF', 'Cu(OH)2'): '2HF + Cu(OH)2 -> 2H2O + CuF2',
            ('HBrO4', 'Cu(OH)2'): '2HBrO4 + Cu(OH)2 -> 2H2O + Cu(BrO4)2',
            ('HIO3', 'Cu(OH)2'): '2HIO3 + Cu(OH)2 -> 2H2O + Cu(IO3)2',
            ('HNO2', 'Cu(OH)2'): '2HNO2 + Cu(OH)2 -> 2H2O + Cu(NO2)2',
            ('HClO3', 'Cu(OH)2'): '2HClO3 + Cu(OH)2 -> 2H2O + Cu(ClO3)2',
            #Fe(OH)2
            ('HCl', 'Fe(OH)2'): '2HCl + Fe(OH)2 -> 2H2O + FeCl2',
            ('HBr', 'Fe(OH)2'): '2HBr + Fe(OH)2 -> 2H2O + FeBr2',
            ('HI', 'Fe(OH)2'): '2HI + Fe(OH)2 -> 2H2O + FeI2',
            ('H2SO4', 'Fe(OH)2'): 'H2SO4 + Fe(OH)2 -> 2H2O + FeSO4',
            ('HNO3', 'Fe(OH)2'): '2HNO3 + Fe(OH)2 -> 2H2O + Fe(NO3)2',
            ('HClO4', 'Fe(OH)2'): '2HClO4 + Fe(OH)2 -> 2H2O + Fe(ClO4)2',
            ('HF', 'Fe(OH)2'): '2HF + Fe(OH)2 -> 2H2O + FeF2',
            ('HBrO4', 'Fe(OH)2'): '2HBrO4 + Fe(OH)2 -> 2H2O + Fe(BrO4)2',
            ('HIO3', 'Fe(OH)2'): '2HIO3 + Fe(OH)2 -> 2H2O + Fe(IO3)2',
            ('HNO2', 'Fe(OH)2'): '2HNO2 + Fe(OH)2 -> 2H2O + Fe(NO2)2',
            ('HClO3', 'Fe(OH)2'): '2HClO3 + Fe(OH)2 -> 2H2O + Fe(ClO3)2',
            #Al(OH)2
            ('HCl', 'Al(OH)2'): '6HCl + 2Al(OH)2 -> 6H2O + 2AlCl3',
            ('HBr', 'Al(OH)2'): '6HBr + 2Al(OH)2 -> 6H2O + 2AlBr3',
            ('HI', 'Al(OH)2'): '6HI + 2Al(OH)2 -> 6H2O + 2AlI3',
            ('H2SO4', 'Al(OH)2'): '3H2SO4 + 2Al(OH)2 -> 6H2O + Al2(SO4)3',
            ('HNO3', 'Al(OH)2'): '6HNO3 + 2Al(OH)2 -> 6H2O + 2Al(NO3)3',
            ('HClO4', 'Al(OH)2'): '6HClO4 + 2Al(OH)2 -> 6H2O + 2Al(ClO4)3',
            ('HF', 'Al(OH)2'): '6HF + 2Al(OH)2 -> 6H2O + 2AlF3',
            ('HBrO4', 'Al(OH)2'): '6HBrO4 + 2Al(OH)2 -> 6H2O + 2Al(BrO4)3',
            ('HIO3', 'Al(OH)2'): '6HIO3 + 2Al(OH)2 -> 6H2O + 2Al(IO3)3',
            ('HNO2', 'Al(OH)2'): '6HNO2 + 2Al(OH)2 -> 6H2O + 2Al(NO2)3',
            ('HClO3', 'Al(OH)2'): '6HClO3 + 2Al(OH)2 -> 6H2O + 2Al(ClO3)3',
            #Na2CO3
            ('HCl', 'Na2CO3'): '2HCl + Na2CO3 -> H2O + CO2 + 2NaCl',
            ('HBr', 'Na2CO3'): '2HBr + Na2CO3 -> H2O + CO2 + 2NaBr',
            ('HI', 'Na2CO3'): '2HI + Na2CO3 -> H2O + CO2 + 2NaI',
            ('H2SO4', 'Na2CO3'): 'H2SO4 + Na2CO3 -> H2O + CO2 + Na2SO4',
            ('HNO3', 'Na2CO3'): '2HNO3 + Na2CO3 -> H2O + CO2 + 2NaNO3',
            ('HClO4', 'Na2CO3'): '2HClO4 + Na2CO3 -> H2O + CO2 + 2NaClO4',
            ('HF', 'Na2CO3'): '2HF + Na2CO3 -> H2O + CO2 + 2NaF',
            ('HBrO4', 'Na2CO3'): '2HBrO4 + Na2CO3 -> H2O + CO2 + 2NaBrO4',
            ('HIO3', 'Na2CO3'): '2HIO3 + Na2CO3 -> H2O + CO2 + 2NaIO3',
            ('HNO2', 'Na2CO3'): '2HNO2 + Na2CO3 -> H2O + CO2 + 2NaNO2',
            ('HClO3', 'Na2CO3'): '2HClO3 + Na2CO3 -> H2O + CO2 + 2NaClO3',
            #K2CO3
            ('HCl', 'K2CO3'): '2HCl + K2CO3 -> H2O + CO2 + 2KCl',
            ('HBr', 'K2CO3'): '2HBr + K2CO3 -> H2O + CO2 + 2KBr',
            ('HI', 'K2CO3'): '2HI + K2CO3 -> H2O + CO2 + 2KI',
            ('H2SO4', 'K2CO3'): 'H2SO4 + K2CO3 -> H2O + CO2 + K2SO4',
            ('HNO3', 'K2CO3'): '2HNO3 + K2CO3 -> H2O + CO2 + 2KNO3',
            ('HClO4', 'K2CO3'): '2HClO4 + K2CO3 -> H2O + CO2 + 2KClO4',
            ('HF', 'K2CO3'): '2HF + K2CO3 -> H2O + CO2 + 2KF',
            ('HBrO4', 'K2CO3'): '2HBrO4 + K2CO3 -> H2O + CO2 + 2KBrO4',
            ('HIO3', 'K2CO3'): '2HIO3 + K2CO3 -> H2O + CO2 + 2KIO3',
            ('HNO2', 'K2CO3'): '2HNO2 + K2CO3 -> H2O + CO2 + 2KNO2',
            ('HClO3', 'K2CO3'): '2HClO3 + K2CO3 -> H2O + CO2 + 2KClO3',
            # Tambahkan entri lain sesuai kebutuhan
        }
        
    # Cek apakah senyawa_asam dan senyawa_basa termasuk asam kuat atau basa kuat
        if senyawa_asam in asam and senyawa_basa in basa:
            # Jika benar, dapatkan hasil reaksi dan senyawa garam
            hasil_reaksi = tabel_hasil_reaksi.get((senyawa_asam, senyawa_basa), None)
            if hasil_reaksi:
                return f"***Reaksi dari:*** {senyawa_asam} + {senyawa_basa} = {hasil_reaksi}\n ***Reaksi sebelah kiri dan kanan kemungkinan belum konstan!***"
            else:
                return "***Senyawa garam atau hasil reaksi tidak terdefinisi (datanya belum dibuat) untuk pasangan asam dan basa ini. silahkan gunakan command !report_reaksi untuk berikan kritikan dan sarannya.***"
        else:
            return "***Reaksi tidak terjadi karena senyawa asam atau basa tidak sesuai.***"

async def setup(bot):
    await bot.add_cog(Chemistry(bot))