

import random
import time
from datetime import datetime


class Sensor:
 

    def __init__(self, nome, tipo, minimo, maximo, seg_min, seg_max, unidade):
        self._nome    = nome
        self._tipo    = tipo
        self._minimo  = minimo
        self._maximo  = maximo
        self._seg_min = seg_min
        self._seg_max = seg_max
        self._unidade = unidade
        self._valor_atual = None

    def gerar_leitura(self):
    
        self._valor_atual = random.uniform(self._minimo, self._maximo)
        return self._valor_atual

    def em_alerta(self):
    
        if self._valor_atual is None:
            return False
        return not (self._seg_min <= self._valor_atual <= self._seg_max)

    def descricao_alerta(self):
      
        if not self.em_alerta():
            return ""
        if self._tipo == "temperatura":
            return "Temperatura acima do permitido!" if self._valor_atual > self._seg_max else "Temperatura abaixo do permitido!"
        elif self._tipo == "umidade":
            return "Umidade muito alta!" if self._valor_atual > self._seg_max else "Umidade muito baixa!"
        elif self._tipo == "luminosidade":
            return "Ambiente muito claro!" if self._valor_atual > self._seg_max else "Ambiente escuro!"
        return "Valor fora do limite!"


    @property
    def nome(self):
        return self._nome

    @property
    def tipo(self):
        return self._tipo

    @property
    def valor_atual(self):
        return self._valor_atual

    @property
    def unidade(self):
        return self._unidade




class SensorTemperatura(Sensor):
    """
    Sensor de temperatura.
    Simulação : 10°C a 45°C
    Faixa segura: 18°C a 28°C
    """
    def __init__(self):
        super().__init__(
            nome="Sensor de Temperatura",
            tipo="temperatura",
            minimo=10.0, maximo=45.0,
            seg_min=18.0, seg_max=28.0,
            unidade="°C"
        )


class SensorUmidade(Sensor):
    """
    Sensor de umidade.
    Simulação : 20% a 100%
    Faixa segura: 40% a 70%
    """
    def __init__(self):
        super().__init__(
            nome="Sensor de Umidade",
            tipo="umidade",
            minimo=20.0, maximo=100.0,
            seg_min=40.0, seg_max=70.0,
            unidade="%"
        )


class SensorLuminosidade(Sensor):
    """
    Sensor de luminosidade.
    Simulação : 0 a 1000 lux
    Faixa segura: 200 a 800 lux
    """
    def __init__(self):
        super().__init__(
            nome="Sensor de Luminosidade",
            tipo="luminosidade",
            minimo=0.0, maximo=1000.0,
            seg_min=200.0, seg_max=800.0,
            unidade="lx"
        )


class Ambiente:


    def __init__(self):
        self.sensores = []

    def adicionar_sensor(self, sensor):
        """Adiciona um sensor ao ambiente."""
        self.sensores.append(sensor)

    def esta_critico(self):
        """Retorna True se qualquer sensor estiver em alerta."""
        return any(sensor.em_alerta() for sensor in self.sensores)

class Monitoramento:
 
    def __init__(self, ambiente, qtd_leituras=50, intervalo=0.5):
        self.ambiente      = ambiente
        self.qtd_leituras  = qtd_leituras
        self.intervalo     = intervalo
        self.historico     = []
        self.total_alertas = 0

    def executar(self):
     
        print("\n Iniciando monitoramento...\n")

        for i in range(1, self.qtd_leituras + 1):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for sensor in self.ambiente.sensores:
                valor  = sensor.gerar_leitura()
                alerta = sensor.em_alerta()

                if alerta:
                    self.total_alertas += 1

                self.historico.append({
                    "timestamp": timestamp,
                    "sensor"   : sensor.nome,
                    "tipo"     : sensor.tipo,
                    "valor"    : valor,
                    "unidade"  : sensor.unidade,
                    "alerta"   : alerta
                })

            self.exibir_dashboard(i, timestamp)

            time.sleep(self.intervalo)

    def exibir_dashboard(self, numero_leitura, timestamp):
        print("\n================ MONITORAMENTO DO AMBIENTE ================")
        print(f"  Leitura nº : {numero_leitura}")
        print(f"  Horário    : {timestamp}\n")

        for sensor in self.ambiente.sensores:
            status = "ALERTA" if sensor.em_alerta() else "OK"
            print(f"  {sensor.nome:25}: {sensor.valor_atual:7.2f} {sensor.unidade:<3}  ->  {status}")
            if sensor.em_alerta():
                print(f"    Mensagem: {sensor.descricao_alerta()}")

        status_ambiente = "CRÍTICO" if self.ambiente.esta_critico() else "SEGURO"
        print(f"\n  Total de leituras : {len(self.historico)}")
        print(f"  Total de alertas  : {self.total_alertas}")
        print(f"  Status do ambiente: {status_ambiente}")
        print("===========================================================")

    def gerar_relatorio_final(self):
 
        dados = {"temperatura": [], "umidade": [], "luminosidade": []}
        for registro in self.historico:
            dados[registro["tipo"]].append(registro["valor"])

        def estatisticas(lista):
            if not lista:
                return 0.0, 0.0, 0.0
            return (
                sum(lista) / len(lista),
                min(lista),
                max(lista)
            )

        temp_media, temp_min, temp_max = estatisticas(dados["temperatura"])
        umi_media,  umi_min,  umi_max  = estatisticas(dados["umidade"])
        lum_media,  lum_min,  lum_max  = estatisticas(dados["luminosidade"])

        status_final = "CRÍTICO" if self.ambiente.esta_critico() else "SEGURO"

        linhas = []
        linhas.append("=" * 60)
        linhas.append("  RELATÓRIO FINAL — SISTEMA DE MONITORAMENTO DE AMBIENTE")
        linhas.append("=" * 60)
        linhas.append("")
        linhas.append(f"  Quantidade total de leituras : {len(self.historico)}")
        linhas.append(f"  Total de alertas gerados     : {self.total_alertas}")
        linhas.append(f"  Status final do ambiente     : {status_final}")
        linhas.append("")
        linhas.append("  TEMPERATURA:")
        linhas.append(f"    Média  : {temp_media:.2f} °C")
        linhas.append(f"    Mínima : {temp_min:.2f} °C")
        linhas.append(f"    Máxima : {temp_max:.2f} °C")
        linhas.append("")
        linhas.append("  UMIDADE:")
        linhas.append(f"    Média  : {umi_media:.2f} %")
        linhas.append(f"    Mínima : {umi_min:.2f} %")
        linhas.append(f"    Máxima : {umi_max:.2f} %")
        linhas.append("")
        linhas.append("  LUMINOSIDADE:")
        linhas.append(f"    Média  : {lum_media:.2f} lx")
        linhas.append(f"    Mínima : {lum_min:.2f} lx")
        linhas.append(f"    Máxima : {lum_max:.2f} lx")
        linhas.append("")
        linhas.append("  Link da simulação:")
        linhas.append("  https://github.com/SEU-USUARIO/sistema-monitoramento-ambiente")
        linhas.append("")
        linhas.append("=" * 60)

        texto_relatorio = "\n".join(linhas)

        print("\n" + texto_relatorio)

        with open("relatorio_monitoramento.txt", "w", encoding="utf-8") as f:
            f.write(texto_relatorio)

        print("\n[OK] Relatório salvo em 'relatorio_monitoramento.txt'.")



def main():
  
    ambiente = Ambiente()

    ambiente.adicionar_sensor(SensorTemperatura())
    ambiente.adicionar_sensor(SensorUmidade())
    ambiente.adicionar_sensor(SensorLuminosidade())

    monitor = Monitoramento(ambiente, qtd_leituras=50, intervalo=0.5)
    monitor.executar()

  
    monitor.gerar_relatorio_final()


if __name__ == "__main__":
    main()

