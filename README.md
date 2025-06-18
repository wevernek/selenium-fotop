# Automação Fotop

Este projeto automatiza a participação em eventos específicos no site [dashboard.fotop.com](https://dashboard.fotop.com) utilizando Selenium WebDriver.

## Funcionalidades

- Acessa eventos pelo ID informado
- Realiza login via cookie salvo no arquivo `.env`
- Aceita termos e confirma participação automaticamente
- Otimizado para máxima velocidade (headless, sem imagens, etc.)

## Pré-requisitos

- Python 3.8+
- Google Chrome instalado
- ChromeDriver compatível com sua versão do Chrome

## Instalação

1. Clone este repositório.
2. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure o arquivo `.env` na raiz do projeto:
   ```
   COOKIE_NAME=perm
   COOKIE_VALUE=seu_valor_de_cookie_aqui
   ```

4. Baixe o [ChromeDriver](https://chromedriver.chromium.org/downloads) e coloque o executável na raiz do projeto.

## Uso

Edite o valor de `id_evento` no início do arquivo `app.py` para o ID do evento desejado.

Execute o script:

```sh
python app.py
```

## Observações

- O script foi otimizado para máxima velocidade, mas o tempo de execução depende da resposta do site.
- Não compartilhe seu arquivo `.env` ou valores de cookie publicamente.

## Licença

Este projeto é apenas para fins educacionais.