import json
from datetime import datetime, time, date

import requests

from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivymd.uix.pickers import MDDatePicker, MDTimePicker

import locale # Importe o módulo locale para formatação de data

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class MyTimePicker(MDTimePicker):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_save=self.format_time)

    def format_time(self, instance, value):
        if value:
            formatted_time = value.strftime('%H:%M')
            self.time = formatted_time
            print(f"Hora selecionada: {formatted_time}")

class TelaInicial(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = MDLabel(text="Agenda", halign="center")
        botao_agendar = MDRaisedButton(text="Agendar Consulta", pos_hint={"center_x": 0.5})
        botao_agendar.bind(on_press=self.Agendamento)

        layout.add_widget(label)
        layout.add_widget(botao_agendar)
        self.add_widget(layout)

    def Agendamento(self, instance):
        self.manager.current = "formulario"

class Formulario(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        layout = BoxLayout(orientation='vertical')

        #Adicione widgets para nome, data, hora, etc
        self.nome_input = MDTextField(hint_text="Nome do Paciente")
        self.datetime_label = MDLabel(text="Escolha a Data e Horario da Consulta", halign="center")
        self.selected_date = None
        self.selected_time = None

        #self.datetime_input = ""

        self.botao_datetime = MDRaisedButton(text="Escolher Data e Horario:", pos_hint={"center_x": 0.5})
        self.botao_datetime.bind(on_press=self.mostrar_datetime_picker)

        botao_confirmar = MDRaisedButton(text="Confirmar Agendamento", pos_hint={"center_x": 0.5})
        botao_confirmar.bind(on_press=self.confirmar_agendamento)

        layout.add_widget(self.nome_input)
        layout.add_widget(self.datetime_label)
        layout.add_widget(self.botao_datetime)

        layout.add_widget(botao_confirmar)
        self.add_widget(layout)

    def mostrar_datetime_picker(self, instance):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save_date)
        date_dialog.open()

    def on_save_date(self, instance, value, date_range):
        self.selected_date = value
        self.mostrar_time_picker(instance)

    def mostrar_time_picker(self, instance):
        if self.selected_date is None:
            return
        time_dialog = MDTimePicker()
        time_dialog.time_format = True
        time_dialog.bind(on_save=self.on_save_time)
        time_dialog.open()

    def on_save_time(self, instance, value):
        self.selected_time = value
        #Aqui assumimos que ambos são chamados em sequencia
        if self.selected_date and self.selected_time:
            combinacao_datetime = datetime.combine(self.selected_date, self.selected_time)
            data_formatada = combinacao_datetime.strftime("%A, %d de %b. %Hh") #Formatação
            self.datetime_label.text = f'Consulta será marcada para: {data_formatada}'
            self.botao_datetime.text = "Alterar Data e Horario"
            

    def confirmar_agendamento(self, instance):
        nome = self.nome_input.text
        if not nome:
            self.mostrar_dialog("Erro", "Por favor, insira o nome do paciente.")
            return

        if not self.selected_date or not self.selected_time:
            self.mostrar_dialog("Erro", "Por favor, escolha uma data e hora para a consulta.")
            return
        
        combinacao_datetime = datetime.combine(self.selected_date, self.selected_time)
        data_hora_am_pm = combinacao_datetime.strftime("%Y-%m-%d %I:%M:%S %p")
    
        dados = {'nome': nome, 'data_hora': data_hora_am_pm}

        try:
            resposta = requests.post('http://127.0.0.1:5000/api/agendar', json=dados)
            resposta.raise_for_status()
            mensagem = resposta.json().get('mensagem', 'Agendamento realizado com sucesso!')
            self.mostrar_dialog("Sucesso", mensagem, auto_dismiss=True)
            self.manager.current = "tela_inicial"
        except Exception as e:
            self.mostrar_dialog("Erro", f"Ocorreu um erro ao salvar os dados: {str(e)}")
            print(f"Erro ao salvar os dados: {str(e)}")

        self.manager.current = "tela_inicial"

    def salvar_dados(self, nome, data_hora):
        try:
            with open('agendamentos.json', 'r') as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            dados = []

        dados.append({
            'nome': nome,
            'data': data_hora
        })

        with open('agendamentos.json', 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)

    def mostrar_dialog(self, titulo, mensagem, auto_dismiss=False):
        if not self.dialog:
            self.dialog = MDDialog(
                title=titulo,
                text=mensagem,
            )
        self.dialog.open()
        if auto_dismiss:
            Clock.schedule_once(lambda dt: self.fechar_dialog(), 3.5)

    def fechar_dialog(self):
        self.dialog.dismiss()
        self.dialog = None

class AgendaApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TelaInicial(name='tela_inicial'))
        sm.add_widget(Formulario(name='formulario'))
        return sm
    
    '''def fazer_requisicao(self, instance):
        try:
            resposta = requests.get('http://127.0.0.1:5000/api/index')
            resposta.raise_for_status()
            dados = resposta.json()
            self.label.text = dados['mensagem']
        except requests.exceptions.RequestException as e:
            self.label.text = f'Erro: {e}'
'''
if __name__ == '__main__':
    AgendaApp().run()