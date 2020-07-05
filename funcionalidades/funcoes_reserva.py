# Este modulo acrescenta funcionalidades para gerenciar as agendas dos restaurantes
# pode ser usada para manter a integridade das reservas e da agenda no geral
from datetime import datetime

if __name__ == "__main__":
    from classes import *
else:
    from funcionalidades.classes import *

def verificar_bissexto(ano):
    if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
        return True
    return False

def calcular_congruencia_zeller(dia,mes,ano):  
    '''
    Acha o dia da semana para qualquer dia, mes e ano informado.
    Retorno possível: 0,1,2,3,4,5,6 onde cada valor corresponde:
    0 -> Sábado; 1 -> Domingo; 2 -> Segunda-Feira; [...] ; 6 -> Sexta-Feira
    Para mais informações pesquise pela Congruência de Zeller e sua implementação em Software
    '''
    if mes == 1: 
        mes = 13
        ano -= 1  

    if mes == 2: 
        mes = 14
        ano -= 1
 
    k = ano%100; 
    j = ano//100; 
    ds = (dia + ((13*(mes + 1))//5) + k + (k//4) + (j//4) + (5*j))%7
    return ds


def realizar_reserva(dados):
    estabelecimento = dados["estabelecimento"]
    data_requisicao = datetime.now()
    cliente = dados["cliente"]
    qtd_pessoas = dados["qtd_pessoas"]
    data_marcada = dados["data_marcada"]
    horario_chegada = dados["horario_chegada"]
    horario_saida = dados["horario_saida"]
    agenda = selecionar_agenda(data_marcada,estabelecimento)
    print(agenda)
    if agenda is not None:
        if validar_horario(agenda,horario_chegada,horario_saida) and +\
            validar_vagas(agenda,qtd_pessoas,estabelecimento,data_marcada,horario_chegada,horario_saida):

            Reserva.create(
                data_requisicao = data_requisicao,
                cliente = cliente,
                estabelecimento = estabelecimento,
                qtd_pessoas = qtd_pessoas,
                data_marcada = data_marcada,
                horario_chegada = horario_chegada,
                horario_saida = horario_saida
            )

            disparar_notificacao(
                data_marcada,
                cliente,
                estabelecimento,
                horario_chegada,
                horario_saida,
                qtd_pessoas,
                data_requisicao
            )

            return True
    
    return False

def selecionar_agenda(data_marcada,estabelecimento):
    dia,mes,ano = data_marcada.split("/")
    dia,mes,ano = int(dia), int(mes), int(ano)

    if validar_data(dia,mes,ano):
        dia_formatado = {0:7, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6}
        num_dia = dia_formatado[calcular_congruencia_zeller(dia,mes,ano)]
        agendas = Agenda.select().where(Agenda.estabelecimento==estabelecimento)
        print("OIIII")
        for i in agendas:
            if str(num_dia) in i.dias:
                return i
    
    return None
       
def validar_data(dia,mes,ano):
    qtd_dias_por_mes = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30,10:31,11:30,12:31}
    mesese = {1:"Janeiro", 2:"Fevereiro", 3:"Março", 4:"Abril", 5:"Maio", 6:"Junho",
         7:"Julho", 8:"Agosto", 9:"Setembro", 10:"Outubro", 11:"Novembro", 12:"Dezembro"}

    if verificar_bissexto(ano):
        qtd_dias_por_mes[2] = 29

    if mes >= 1 and mes <= 12 and dia >=1 and dia <= qtd_dias_por_mes[mes] and ano >= datetime.now().year:
        return True
    return False

def validar_horario(agenda,horario_chegada,horario_saida):
    abre = datetime.strptime(agenda.hora_inicio, '%H:%M').time()
    fecha = datetime.strptime(agenda.hora_termino, '%H:%M').time()

    horario_chegada = datetime.strptime(horario_chegada, '%H:%M').time()
    horario_saida = datetime.strptime(horario_saida, '%H:%M').time()

    return horario_chegada >= abre and horario_chegada < fecha and horario_saida > abre and horario_saida < fecha 

def validar_vagas(agenda,qtd_pessoas,estabelecimento,data_marcada,horario_chegada,horario_saida):
    reservas = Reserva.select().where((Reserva.estabelecimento==estabelecimento)
                                        & (Reserva.data_marcada==data_marcada))
    contador = qtd_pessoas
    
    hc = datetime.strptime(horario_chegada, '%H:%M').time()
    hs = datetime.strptime(horario_saida, '%H:%M').time()

    for i in reservas:
        hci = datetime.strptime(i.horario_chegada, '%H:%M').time()
        hsi = datetime.strptime(i.horario_saida, '%H:%M').time()
        
        if hci >= hc and hsi <= hs:
            contador += i.qtd_pessoas
        elif hc <= hsi:
            contador += i.qtd_pessoas
        elif hs >= hci:
            contador += i.qtd_pessoas

    return contador <= agenda.lotacao_maxima_permitida   

def disparar_notificacao(data_marcada,cliente,estabelecimento,
                            horario_chegada,horario_saida,qtd_pessoas,data_requisicao,confirmar=1):
    
    descricao = f'''Sobre a Reserva
                Detalhes:
                Data - {data_marcada}
                Estabelecimento - {estabelecimento.nome_ficticio}
                Horario Chegada - {horario_chegada}
                Horario Saida - {horario_saida}
                Quantidade Pessoas - {qtd_pessoas}
                
                Status
            '''
    if confirmar == 1:
        descricao += "Aguradando Confirmacao do Estabelecimento\n"
    else:
        descricao += "RESERVA CONFIRMADA\n"

    descricao += f"Reserva Gerada em: {data_requisicao}"

    notificacao = Notificacao.create(
                    descricao = descricao,
                    data_envio = datetime.now(),
                    cliente = cliente.email,
                    origem = "Sistema")

def confirmar_reserva(id_reserva):
    try:
        reserva = Reserva.get_by_id(id_reserva)
        reserva.confirmacao = True
        reserva.save()

        disparar_notificacao(
            reserva.data_marcada,
            reserva.cliente,
            reserva.estabelecimento,
            reserva.horario_chegada,
            reserva.horario_saida,
            reserva.qtd_pessoas,
            reserva.data_requisicao,
            confirmar=0
        )
        return True
    except:
        return False

if __name__ =="__main__":
    db.connect()
    estabelecimento = Estabelecimento.select().where(Estabelecimento.cnpj=="42.318.949/0001-84")[0]
    cliente = Cliente.select().where(Cliente.cpf=="111.111.111-11")[0]
    
    dados = {
        "cliente": cliente,
        "estabelecimento": estabelecimento,
        "qtd_pessoas": 4,
        "data_marcada": "10/07/2020",
        "horario_chegada": "18:30",
        "horario_saida": "19:30",
    }

    print(realizar_reserva(dados))

    dados = {
        "cliente": cliente,
        "estabelecimento": estabelecimento,
        "qtd_pessoas": 5,
        "data_marcada": "10/07/2020",
        "horario_chegada": "18:30",
        "horario_saida": "19:30",
    }
    
    print(realizar_reserva(dados))
    print(confirmar_reserva(3),end="\n"*2)
    notificacoes = Notificacao.select()
    for i in notificacoes:
        print(i.descricao,end="\n"*3) 