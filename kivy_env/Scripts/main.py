from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivy.core.window import Window

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
        sm = ScreenManager()
        sm.add_widget(HelpDeskApp(name='helpdesk'))
        sm.add_widget(AbrirChamado(name='chamado'))
    
        return sm
    
class HelpDeskApp(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing='12dp', padding='24dp')
        titulo = MDLabel(text='HelpDask', font_style='H5', halign='center')
        botao = MDRaisedButton(text='Abrir Chamado', on_press=self.abrir_chamado)

        layout.add_widget(titulo)
        layout.add_widget(botao)

        self.add_widget(layout)

    def abrir_chamado(self, instance):
        self.manager.current = "chamado"

class AbrirChamado(MDScreen):
    usuario = 'Rafael'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', spacing='12dp', padding='24dp')
        id_usuario = MDLabel(text=f'{self.usuario}', font_style='H5', halign='left')
        motivo = MDLabel(text='Escolha o motivo para o abrir o chamado')

        #Definir botão de motivo como um atributo da classe
        self.button_chamado = MDRaisedButton( text='Motivo', on_press=self.abrir_meu_motivo)
        self.descricao_chamado = MDTextField(hint_text='Descreva o problema')
        button_confirmacao = MDRaisedButton(text='Confirmar Chamado', on_press=self.confirmar_chamado)

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
        self.manager.current = "helpdesk"

    


if __name__ == '__main__':
    MyApp().run()


