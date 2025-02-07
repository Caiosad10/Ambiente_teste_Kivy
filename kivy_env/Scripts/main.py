from kivymd.tools.hotreload.app import MDApp

import json
import requests

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.toolbar import MDTopAppBar
from kivy.graphics import Color, Rectangle, RoundedRectangle

import os
import time


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
    def build(self, first=False):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"

        sm = ScreenManager()
        self.gerenciador = GerenciadorChamados()

        sm.add_widget(HelpDeskApp(name='helpdesk'))
        sm.add_widget(AbrirChamado(self.gerenciador, name='chamado'))
        sm.add_widget(ListaChamados(self.gerenciador, name='lista_chamados'))

        return sm
    
class HelpDeskApp(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0,0,0,1) # preto
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        
        layout = MDFloatLayout()
        toolbar = MDTopAppBar(
            title="HelpDesk",
            elevation=4,
            pos_hint={'top': 1},
            size=(dp(200), dp(50)),
            md_bg_color=get_color_from_hex("#121212"),
            specific_text_color=get_color_from_hex("#1DB954"), #fonte verde
            left_action_items=[["menu", lambda x: self.abrir_menu()]],
            right_action_items=[["account", lambda x: self.abrir_perfil()]]
        )


        botao_abrir_chamado = MDRaisedButton(
            text='Abrir Chamado',
            md_bg_color=get_color_from_hex("#1DB954"), 
            size_hint=(None, None),
            size = (dp(200), dp(50)),
            pos_hint = {'center_x': 0.5, 'center_y': 0.6},
            on_press=self.abrir_chamado)
        botao_meus_chamados = MDRaisedButton(
            text='Meus Chamados', 
            md_bg_color=get_color_from_hex("#1DB954"),
            size_hint=(None, None),
            size = (dp(200), dp(50)),
            pos_hint = {'center_x': 0.5, 'center_y': 0.4}, 
            on_press=self.ver_chamados)

        layout.add_widget(toolbar)
        layout.add_widget(botao_abrir_chamado)
        layout.add_widget(botao_meus_chamados)

        self.add_widget(layout)

    def abrir_chamado(self, instance):
        self.manager.current = "chamado"

    def ver_chamados(self, instance):
        self.manager.current = "lista_chamados"

    def _update_rect(self, instance, value):
            self.rect.pos = self.pos
            self.rect.size = self.size

    def abrir_menu(self):
        pass

    def abrir_perfil(self):
        pass

class AbrirChamado(MDScreen):
    #dialog = None
    usuario = 'Rafael'
    def __init__(self, gerenciador_chamados, **kwargs):
        super().__init__(**kwargs)
        self.gerenciador_chamados = gerenciador_chamados

        

        layout_principal = MDBoxLayout(orientation='vertical', spacing='12dp', padding='24dp', md_bg_color=get_color_from_hex("#332525"))
        layout_secundario = MDFloatLayout()

        id_usuario = MDLabel(text=f'Usuario: {self.usuario}', font_style='H6', halign='center', theme_text_color='Secondary', pos_hint={'center_x': 0.5,'top': 0.9})

        #Definir botão de motivo como um atributo da classe
        self.button_chamado = MDRaisedButton(
            text='Escolha o motivo',
            md_bg_color=get_color_from_hex("#1DB954"),
            size_hint=(None, None),
            size = (dp(200), dp(50)),
            pos_hint = {'center_x': 0.5, 'top': 0.8},  
            on_press=self.abrir_meu_motivo)
        
        self.descricao_chamado = MDTextField(
            hint_text='Descreva o problema',
            multiline=True,
            size_hint=(None, None),
            size = (dp(200), dp(50)),
            pos_hint = {'center_x': 0.5, 'top': 0.6},
            )
        
        button_confirmacao = MDRaisedButton(
            text='Confirmar Chamado', 
            md_bg_color=get_color_from_hex("#FFA000"),
            size_hint=(None, None),
            size = (dp(200), dp(50)),
            pos_hint = {'center_x': 0.5, 'top': 0.2},  
            on_press=self.confirmar_chamado
            )

        layout_principal.add_widget(id_usuario)
        layout_secundario.add_widget(self.button_chamado)
        layout_secundario.add_widget(self.descricao_chamado)
        layout_secundario.add_widget(button_confirmacao)

        layout_principal.add_widget(layout_secundario)
        self.add_widget(layout_principal)

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
                text_color= get_color_from_hex("#FFFFFF"),
                font_size= '14sp',
                shorten=False,
                max_lines=1
            ),
            md_bg_color= get_color_from_hex("#4CAF50"),
            size_hint=(None, None),
            size=(dp(275), dp(50)),
            pos_hint={"right": 0.95, "top": 0.89},
        )
        
        
        self.snackbar.open()

class ListaChamados(MDScreen):
    def __init__(self, gerenciador_chamados, **kwargs):
        super().__init__(**kwargs)
        self.gerenciador_chamados = gerenciador_chamados

        layout_principal = MDBoxLayout(orientation='vertical', spacing='12dp', padding='24dp', md_bg_color=get_color_from_hex("#332525"))
        titulo = MDLabel(text="Meus Chamados", font_style="H5", halign="center", theme_text_color="Secondary", font_size='18sp', size_hint_y=None, height=dp(40))

        self.data_table = MDDataTable(
            size_hint= (1, 0.7),
            use_pagination=True,
            check=True,
            column_data=[
                ("ID", dp(20)),
                ("Motivo", dp(30)),
                ("Descrição", dp(30)),
                ("Status", dp(20)),
                ("Ações", dp(20)) #Coluna para os botões
            ],
            row_data=self.carregar_chamados(),
            rows_num=5,
            elevation=2
        )
        '''self.scroll_view = MDScrollView()
        self.lista = MDList()
        self.scroll_view.add_widget(self.lista)
'''
        botao_voltar = MDRaisedButton(text="Voltar", md_bg_color=get_color_from_hex("#D32F2F"), on_press=self.voltar, size_hint_x=1)

        layout_principal.add_widget(titulo)
        layout_principal.add_widget(self.data_table)
        layout_principal.add_widget(botao_voltar)

        self.add_widget(layout_principal)

    def carregar_chamados(self):
        chamados = self.gerenciador_chamados.listar_chamados()
        data = []
        for chamado in chamados:
            '''editar = MDRaisedButton(text='Editar', on_press=lambda x, chamado=chamado: self.editar_chamado(chamado))
            excluir = MDRaisedButton(text='Excluir', on_press=lambda x, chamado=chamado: self.excluir_chamado(chamado))'''
            data.append([chamado['id'], chamado['motivo'], chamado['descricao'], chamado['status'], "Editar | Excluir"])
        return data
        
    def voltar(self, instance):
        self.manager.current = "helpdesk"

    def on_pre_enter(self):
        self.data_table.row_data = self.carregar_chamados()

    def on_row_press(self, instance_table, instance_row):
        print(f"Linha {instance_row.index} pressionada")

    def editar_chamado(self, chamado):
        print(f"Editar chamado {chamado['id']}")

    def excluir_chamado(self, chamado):
        print(f"Excluir chamado {chamado['id']}")

if __name__ == '__main__':
    MyApp().run()


