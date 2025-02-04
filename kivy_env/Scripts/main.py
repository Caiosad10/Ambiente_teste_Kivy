from kivymd.app import MDApp

import json
import requests

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivymd.uix.responsivelayout import MDResponsiveLayout



class GerenciadorChamados:
    def __init__(self):
        self.chamados = []

    def adicionar_chamado(self, usuario, motivo, descricao):
        chamado = {
            "id": len(self.chamados) + 1,
            "usuario": usuario,
            "motivo": motivo,
            "descricao": descricao,
            "status": "Aberto"
        }
        self.chamados.append(chamado)
        print(f"Chamado {chamado['id']} adicionado com sucesso!")

    def listar_chamados(self):
        return self.chamados

class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        sm = ScreenManager()
        self.gerenciador = GerenciadorChamados()

        sm.add_widget(HelpDeskApp(name='helpdesk'))
        sm.add_widget(AbrirChamado(self.gerenciador, name='chamado'))
        sm.add_widget(ListaChamados(self.gerenciador, name='lista_chamados'))

        return sm
    
class HelpDeskApp(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing='12dp', padding='24dp')
        titulo = MDLabel(text='HelpDask', font_style='H4', halign='center', theme_text_color='Primary')
        botao_abrir_chamado = MDRaisedButton(text='Abrir Chamado', md_bg_color=get_color_from_hex("#1976D2"), on_press=self.abrir_chamado)
        botao_meus_chamados = MDRaisedButton(text='Meus Chamados', md_bg_color=get_color_from_hex("#388E3C"), on_press=self.ver_chamados)

        layout.add_widget(titulo)
        layout.add_widget(botao_abrir_chamado)
        layout.add_widget(botao_meus_chamados)

        self.add_widget(layout)

    def abrir_chamado(self, instance):
        self.manager.current = "chamado"

    def ver_chamados(self, instance):
        self.manager.current = "lista_chamados"


class AbrirChamado(MDScreen):
    #dialog = None
    usuario = 'Rafael'
    def __init__(self, gerenciador_chamados, **kwargs):
        super().__init__(**kwargs)
        self.gerenciador_chamados = gerenciador_chamados

        

        layout = MDBoxLayout(orientation='vertical', spacing='12dp', padding='24dp')
        id_usuario = MDLabel(text=f'Usuario: {self.usuario}', font_style='H6', halign='left', theme_text_color='Secondary')
        motivo = MDLabel(text='Escolha o motivo para do chamado:', theme_text_color='Hint')

        #Definir botão de motivo como um atributo da classe
        self.button_chamado = MDRaisedButton( text='Motivo', on_press=self.abrir_meu_motivo)
        self.descricao_chamado = MDTextField(hint_text='Descreva o problema')
        button_confirmacao = MDRaisedButton(text='Confirmar Chamado', md_bg_color=get_color_from_hex("#FFA000"), on_press=self.confirmar_chamado)

        layout.add_widget(id_usuario)
        layout.add_widget(motivo)
        layout.add_widget(self.button_chamado)
        layout.add_widget(self.descricao_chamado)
        layout.add_widget(button_confirmacao)

        self.add_widget(layout)

        self.menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Problema com a conexão",
                "on_release": lambda x="Problema com a conexão": self.selecionar_motivo(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Problema com o site",
                "on_release": lambda x="Problema com o site": self.selecionar_motivo(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Problema com o aplicativo",
                "on_release": lambda x="Problema com o aplicativo": self.selecionar_motivo(x),
            }
        ]

        self.menu_motivo = MDDropdownMenu(
            caller= self.button_chamado,
            items=self.menu_items,
            width_mult=4,
        )

    def abrir_meu_motivo(self, instance):
        self.menu_motivo.caller = instance
        self.menu_motivo.open()

    def selecionar_motivo(self, motivo):
        print(f"motivo selecionado: {motivo}")
        self.button_chamado.text = motivo
        self.menu_motivo.dismiss()

    def confirmar_chamado(self, instance):
        motivo = self.button_chamado.text  # Obtém o motivo selecionado
        descricao = self.descricao_chamado.text  # Obtém a descrição do chamado

        self.gerenciador_chamados.adicionar_chamado(self.usuario, motivo, descricao)

        self.exibir_snackbar()

        self.manager.current = "helpdesk"

    def exibir_snackbar(self):
        self.snackbar = MDSnackbar(
            MDLabel(
                text="Chamado aberto com sucesso!",
                theme_text_color="Custom",
                text_color= get_color_from_hex("#FFFFFF")
            ),
            md_bg_color= get_color_from_hex("#4CAF50"),
            width = 500,
            height = 100,
            size_hint_x = None
        )
        
        self.snackbar.pos_hint = {"right": 1, "top": 1}
        self.snackbar.x = self.width - self.snackbar.width - 10
        self.snackbar.open()

class ListaChamados(MDScreen):
    def __init__(self, gerenciador_chamados, **kwargs):
        super().__init__(**kwargs)
        self.gerenciador_chamados = gerenciador_chamados

        layout = MDBoxLayout(orientation='vertical', spacing='12dp', padding='24dp')
        titulo = MDLabel(text="Meus Chamados", font_style="H5", halign="center")

        self.scroll_view = MDScrollView()
        self.lista = MDList()
        self.scroll_view.add_widget(self.lista)

        botao_voltar = MDRaisedButton(text="Voltar", md_bg_color=get_color_from_hex("#D32F2F"), on_press=self.voltar)

        layout.add_widget(titulo)
        layout.add_widget(self.scroll_view)
        layout.add_widget(botao_voltar)

        self.add_widget(layout)

    def on_enter(self):
        self.carregar_chamados()

    def carregar_chamados(self):
        self.lista.clear_widgets()
        for chamado in self.gerenciador_chamados.listar_chamados():
            item = OneLineListItem(text=f"ID {chamado['id']} - {chamado['motivo']}: {chamado['descricao']} - Status: {chamado['status']}")
            self.lista.add_widget(item)
        
    def voltar(self, instance):
        self.manager.current = "helpdesk"

if __name__ == '__main__':
    MyApp().run()


