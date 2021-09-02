# yonde!
**yonde! (読んで!)** é um mangá downloader (para leitura offline) voltado para sites e scans brasileiros. Também permite que você converta os capítulos baixados para um arquivo PDF maciço para facilitar a leitura em diferentes dispositivos. 

- [Instalação](#instalação)
- [Sites suportados](#sites-suportados)
- [Opções](#opções)
- [Changelog](#changelog)
- [Baixando mangás](#baixando-mangás)
- [Contribuindo](#contribuindo)
- [Avisos](#avisos)
- [Manifesto](#manifesto)

## Instalação
``yonde!`` requer Python 3.7+

Use o `pip` pra instalar o pacote do PyPI:

```bash
pip install yonde
```

ou:

```bash
pip3 install yonde
```

## Sites suportados
Você pode ver a lista de sites suportados pelo **yonde!** [aqui](https://github.com/yonde-manga/yonde/blob/main/PROVIDERS.md).

## Opções
    -h, --help                           Mostra essa mensagem de ajuda.
    
    -u, --url URL                        URL do mangá que será baixado. Suporta
                                         um capítulo específico ou a página do
                                         mangá contendo todos os capítulos.
                                         
    -t, --threads NÚMERO                 Número de threads que serão utilizadas
                                         para baixar as imagens dos capítulos.
                                         
    -o, --output PATH                    Caminho aonde o mangá (PDF e/ou imagens)
                                         será baixado.
                                         
    -i, --inicial NÚMERO                 Baixar a partir de determinado capítulo.
    
    -f, --final NÚMERO                   Baixar até determinado capítulo.
    
    --typo TYPO                          Tipo de download que será realizado.
                                         Disponíveis: "pdf" e "imagens".
                                         
    --no-banner                          Não mostrar o banner.

## Changelog
Você pode checar o changelog [aqui](https://github.com/yonde-manga/yonde/blob/main/CHANGELOG.md).

## Baixando mangás
    # Baixando todos os capítulos de um mangá
    yonde -u "https://unionmangas.top/pagina-manga/kimetsu-no-yaiba"
    
    # Baixando do capítulo 10 ao capítulo 20 e salvando em /minha/pasta/de/mangas
    yonde -u "https://www.brmangas.com/mangas/tokyo-revengers-online/" -i 10 -f 20 -o /minha/pasta/de/mangas
    
    # Baixando até o capítulo 100 utilizando 20 threads e salvando em /minha/pasta/de/mangas
    yonde -u "https://goldenmanga.top/mangabr/solo-leveling-gm" -f 100 -o /minha/pasta/de/mangas -t 20
    
    # Baixando e convertendo para PDF um capítulo específico
    yonde -u "https://mangahost4.com/manga/vinland-saga-mh41987/extra-01" --typo pdf

## Contribuindo
Por favor, contribua! Se você encontrou um bug, quer sugerir melhorias ou adicionar novos recursos ao projeto, abra uma [issue](https://github.com/yonde-manga/yonde/issues). Você também pode contribuir recomendando o projeto para amigos; desta maneira, mais pessoas terão ciência do projeto, maior ele se tornará e mais sites ele suportará.

## Avisos
> A criação do PDF dos capítulos envolve um processo de conversão das imagens que exige um pouco mais de poder de processamento. Leve isso em conta ao rodar o **yonde!** utilizando a flag `--typo` com o valor "pdf" (principalmente rodando várias instâncias do programa). Por padrão, essa flag recebe o valor "imagens". Você pode checar o processo de conversão [aqui](https://github.com/yonde-manga/yonde/blob/2f36f816d328dc6c4cee7b679fefe250fe27b5a1/yonde/images/images.py#L44).

> Por conta da lógica de intervalos de capítulos do **yonde!** ser definida por valores exatos, capítulos com nomenclatura "especial" não serão incluídos ao baixar definindo-se um intervalo (por exemplo: "especial-01", "extra-01", "extra-sj"). Porém, você pode baixar este capítulo em específico passando a URL dele na flag `-u` ou `--url`.

## Manifesto
O **yonde!** é um programa simples e de código aberto que tem como objetivo facilitar a leitura de mangás. O projeto nasceu também como alternativa às condições impostas pelos sites para a visualização (e quando possível, download) de obras. O projeto é totalmente transparente, sinta-se livre para ler todo o código antes de rodá-lo na sua máquina e, caso não haja clareza em algum ponto do código, para abrir uma issue questionando.
