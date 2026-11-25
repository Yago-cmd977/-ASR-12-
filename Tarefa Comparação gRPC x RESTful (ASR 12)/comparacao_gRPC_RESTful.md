# Comparação gRPC x RESTful (ASR 12)

## 1. Comparação com base nos exemplos

**Modelo de programação.** No RESTful, o cliente manipula *recursos* identificados por URLs (`/empdb/employee/201`) usando verbos HTTP fixos (GET, POST, PUT, DELETE). No gRPC, o cliente chama *procedimentos remotos* com nomes específicos da aplicação (`CreateEmployee`, `UpdateEmployeeTitle`), como se fossem métodos locais. Por isso, o RESTful usa uma interface genérica e o gRPC uma interface específica da aplicação, definida no arquivo `.proto`.

**Eficiência.** O gRPC usa HTTP/2, que permite multiplexação de várias requisições em uma só conexão, e serialização binária com Protocol Buffers, mais compacta e rápida de processar do que o JSON textual do RESTful. Em trocas frequentes de mensagens pequenas entre serviços, isso reduz latência e tráfego. O RESTful, por outro lado, usa HTTP/1.1 na prática e JSON legível, o que custa mais em tamanho e processamento, mas é suficiente para a maioria dos casos.

**Modularidade.** No gRPC, o contrato (`EmployeeService.proto`) é o ponto central: cliente e servidor são gerados a partir dele, e a mudança de um campo exige regenerar o código. No RESTful, o contrato é implícito nas rotas e no formato dos dados, e cada endpoint pode evoluir separadamente.

**Manutenibilidade.** O gRPC oferece verificação de tipos em tempo de compilação e geração automática de código, o que reduz erros de integração. O RESTful é mais simples de depurar: basta um navegador, `curl` ou um cliente HTTP comum para inspecionar as requisições. No exemplo, a interface gRPC não tem salário nem média, então para estendê-la seria preciso alterar o `.proto`, regenerar os stubs e ajustar servidor e cliente. No RESTful, essas mudanças ficaram restritas a `EmployeeService.py`.

**Abertura.** O RESTful é baseado em padrões amplamente adotados (HTTP, URLs, JSON) e pode ser consumido por qualquer linguagem e por navegadores sem ferramentas especiais. O gRPC exige geração de código por linguagem e suporte a HTTP/2 que nem todos os navegadores e proxies oferecem plenamente (o uso em navegadores passa por gRPC-Web).

**Transparência de distribuição.** No gRPC, a chamada remota parece local no código do cliente (stubs), o que esconde a distribuição de forma mais forte, mas também pode levar o programador a esquecer latência e falhas parciais. No RESTful, a natureza remota é explícita: o cliente monta a URL, trata códigos HTTP (como os 404 e 409 implementados) e lida com timeouts. Essa explicitude é uma vantagem didática e de controle, embora torne o código do cliente mais verboso.

## 2. APIs para frontend e backend

Para **APIs voltadas ao frontend** (aplicações web e móveis que consomem dados do usuário), o RESTful costuma ser a escolha mais adequada: é suportado nativamente por navegadores, facilita o cache HTTP, é fácil de documentar e de testar, e a equipe de frontend pode consumi-lo sem depender de ferramentas de geração de código. O gRPC, nesse cenário, exige uma camada de tradução (gRPC-Web ou um gateway) e oferece pouco ganho, já que a latência de rede costuma dominar.

Para **APIs de comunicação entre serviços no backend** (microsserviços internos, alto volume de chamadas, baixa latência), o gRPC tende a ser superior: a serialização binária, o HTTP/2, o contrato forte e o *streaming* bidirecional reduzem custo e acoplamento incorreto entre serviços. O RESTful continua válido aqui, mas com maior overhead.

Uma arquitetura comum combina os dois: REST na borda (frontend e clientes externos) e gRPC internamente entre os serviços.

## 3. Fatores a considerar ao escolher uma tecnologia

- **Quem consome a API:** navegadores e terceiros favorecem REST; serviços internos favorecem gRPC.
- **Desempenho exigido:** volume alto de chamadas pequenas e baixa latência favorecem gRPC.
- **Tipo de interação:** necessidade de streaming contínuo favorece gRPC; operações CRUD sobre recursos favorecem REST.
- **Interoperabilidade e abertura:** REST é universal; gRPC exige geração de código e suporte a HTTP/2.
- **Evolução e versionamento:** o `.proto` facilita a evolução controlada em gRPC; em REST, o versionamento é feito por convenção (ex.: `/v1/`).
- **Facilidade de depuração e ferramentas:** REST é mais fácil de inspecionar e testar manualmente.
- **Experiência da equipe e ecossistema:** a familiaridade com a tecnologia e as ferramentas disponíveis pesa na decisão.
- **Cache e infraestrutura:** REST se beneficia diretamente de caches HTTP, proxies e CDNs.
