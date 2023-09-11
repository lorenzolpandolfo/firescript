import re

class Formatting:
    def __init__(self):
        pass

    def checar_se_ha_numero(self, linha):
        return any(c.isdigit() for c in linha)


    def remover_espacos_desnecessarios(self, linha) -> str:
        linha = re.sub(r'\s+', ' ', linha)
        return linha.strip()
    
    def remover_emojis(self, texto) -> str:
        emojis = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # símbolos & pictografias
                            u"\U0001F680-\U0001F6FF"  # transportes & símbolos de mapas
                            u"\U0001F1E0-\U0001F1FF"  # bandeiras (iOS)
                            u"\U00002500-\U00002BEF"  # caracteres chineses comuns
                            u"\U00002702-\U000027B0"  # símbolos diversos
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            u"\U0001f926-\U0001f937"
                            u"\U00010000-\U0010ffff"
                            u"\u200d"
                            u"\u2640-\u2642"
                            u"\u2600-\u2B55"
                            u"\u23cf"
                            u"\u23e9"
                            u"\u231a"
                            u"\ufe0f"  # dingbats
                            u"\u3030"
                            "]+", flags=re.UNICODE)

        return emojis.sub(r'', texto).strip()

    def escrever_correcoes(self, novo: list) -> None:
        with open("numeros.txt", "w+", encoding="utf8") as arquivo:
            for linha in novo:
                if '\n' in linha:
                    arquivo.writelines(linha)
                else:
                    arquivo.writelines(linha + '\n')

    def corrigir_erros(self) -> None:
        with open("numeros.txt", "r+", encoding='utf8') as arquivo:
            linhas = arquivo.readlines()
            conserto = []
            numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

            for i, linha in enumerate(linhas):
                linha = self.remover_espacos_desnecessarios(linha.replace("-", "").replace("(", "").replace(")", "")).replace("+", "")

                if self.checar_se_ha_numero(linha):
                    if ',' in linha:
                        numero = linha.split(",")[1]
                        # formatando o numero corretamente
                        numero = re.sub(r'\D', '', numero)
                        # formatando o nome corretamente
                        nome = linha.split(",")[0].strip()
                        # adicionando a virgula na linha, com nome e numero formatados corretamente
                        linha = nome + f", {numero}"
                        # removendo emojis da linha
                        linha_formatada = self.remover_emojis(linha.replace("\n", ""))
                        # adiciona na lista para ser escrito no arquivo
                        conserto.append(linha_formatada)
                    else:
                        # Encontrar o local correto onde a virgula deveria estar e adiciona-la
                        linha_list = list(linha)

                        try:
                            # para cada caractere da linha
                            for localindex, c in enumerate(linha):
                                proximo_caractere = linha_list[localindex + 1]

                                # encontra o local para inserir a virgula (numero seguido de outro numero)
                                if c in numeros and proximo_caractere in numeros:

                                    # caso o caractere anterior à nova virgula seja espaço, remove-o
                                    if linha_list[localindex - 1] == ' ':
                                        linha_list[localindex - 1] = ''

                                    # formata a linha com a virgula
                                    linha_list[localindex] = f', {linha_list[localindex]}'
                                    linha = ''.join(linha_list)

                                    nome = linha.split(",")[0]
                                    numero = linha.split(",")[1]
                                    numero = re.sub(r'\D', '', numero)

                                    linha = nome + f', {numero}'

                                    # remove emojis da linha
                                    linha_formatada = self.remover_emojis(linha)

                                    # deixa o primeiro caractere do nome maiusculo
                                    linha_formatada_list = list(linha_formatada)
                                    linha_formatada_list[0] = str(linha_formatada_list[0]).upper()
                                    linha_formatada = ''.join(linha_formatada_list)

                                    # adiciona à lista que sera escrita
                                    conserto.append(linha_formatada)
                                    break

                        # caso não haja numero seguido de numero na linha
                        except IndexError:
                            print(f"[X] A linha foi removida: {linha}")
                else:
                    print(f"[X] A linha foi removida: {linha} (não há número de telefone)")
                # salva no arquivo a lista de linhas consertadas
                self.escrever_correcoes(conserto)