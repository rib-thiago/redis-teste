# Propostas de Cenários para Diagramas de Casos de Uso

## 1. **Cenário: Upload de Arquivos e Criação de Coleções:**

1. **Ator Principal:** Usuário
2. **Casos de Uso:**
   i. **Realizar Upload de Arquivo:** O usuário faz o upload de um arquivo (imagem ou PDF).
   ii. **Criar Coleção:** O usuário cria uma nova coleção e associa o arquivo enviado a essa coleção.
3. **Elementos Relevantes:**
   1. Interface de Upload
   2. Controlador (Flask)
   3. Serviço de Upload
   4. Model (MongoDB)
   5. Interface de Criação de Coleção

---

## 2. **Cenário: Edição de Documentos na Coleção**

1. **Ator Principal:** Usuário
2. **Casos de Uso:**
   i. **Visualizar Documento:** O usuário visualiza um documento existente na coleção.
   ii. **Editar Documento:** O usuário realiza edições no documento.
   iii. **Salvar Edições:** O usuário salva as edições feitas no documento.
3. **Elementos Relevantes:**
   1. Interface de Visualização/Edição
   2. Controlador (Flask)
   3. Serviço de Edição
   4. Model (MongoDB)
   5. Possivelmente Cache (Redis) para otimização

---

## 3. **Cenário: Gerenciamento de Acesso a Coleções**

1. **Ator Principal:** Usuário com permissões de gerenciamento
2. **Casos de Uso:**
   i. **Definir Acesso:** O usuário define permissões de acesso para outros usuários em uma coleção.
   ii. **Revogar Acesso:** O usuário revoga permissões de acesso previamente concedidas.
3. **Elementos Relevantes:**
   1. Interface de Gerenciamento de Acesso
   2. Controlador (Flask)
   3. Serviço de Gerenciamento de Acesso
   4. Model (MongoDB)
   5. Possivelmente Cache (Redis) para otimização

---

## 4. **Cenário: Tradução de Texto em Documentos**

1. **Ator Principal:** Usuário
2. **Casos de Uso:**
   i. **Selecionar Texto:** O usuário seleciona o texto a ser traduzido em um documento.
   ii. **Realizar Tradução:** O usuário escolhe a opção de traduzir o texto selecionado.
3. **Elementos Relevantes:**
   1. Interface de Visualização/Edição
   2. Controlador (Flask)
   3. Serviço de Tradução
   4. Model (MongoDB)
   5. Possivelmente Cache (Redis) para otimização

---

## 5. **Cenário: Aplicação de Edições em Lote**

1. **Ator Principal:** Usuário
2. **Casos de Uso:**
   i. **Selecionar Documentos:** O usuário seleciona os documentos em uma coleção.
   ii. **Escolher Edições em Lote:** O usuário escolhe as edições a serem aplicadas em lote.
   iii. **Aplicar Edições:** O usuário aplica as edições escolhidas em todos os documentos selecionados.
3. **Elementos Relevantes:**
   1. Interface de Visualização/Edição
   2. Controlador (Flask)
   3. Serviço de Edição em Lote
   4. Model (MongoDB)
   5. Possivelmente Cache (Redis) para otimização

---

## 6. **Cenário: Pesquisa de Coleções de Imagens**

1. **Ator Principal:** Usuário
2. **Casos de Uso:**
   i. **Realizar Pesquisa:** O usuário interage com a interface da aplicação, digitando um termo de pesquisa.
   ii. **Enviar Solicitação de Pesquisa:** A interface envia uma solicitação para a Controller responsável por lidar com a pesquisa.
   iii. **Iniciar Busca:** A Controller inicia a busca por coleções relacionadas ao termo de pesquisa.
   iv. **Buscar Informações no MongoDB:** A Controller solicita ao MongoDB para buscar as informações das coleções relevantes.
   v. **Retornar Resultados do MongoDB:** O MongoDB retorna os resultados da busca.
   vi. **Processar Resultados:** A Controller processa os resultados e cria objetos Model representando as coleções.
   vii. **Decidir Estratégia de Caching:** A Controller decide qual estratégia de caching utilizar e envia uma solicitação ao RedisCache.
   viii. **Verificar Cache no Redis:** O RedisCache verifica se os dados estão em cache e retorna os dados se estiverem disponíveis.
   ix. **Solicitar Dados à Controller:** Caso não haja dados em cache, o RedisCache solicita os dados à Controller.
   x. **Buscar Dados no MongoDB Novamente:** A Controller solicita novamente ao MongoDB e armazena os resultados no cache.
   xi. **Armazenar Dados no Cache:** O RedisCache armazena os resultados em cache.
   xii. **Retornar Resultados à Interface:** A Controller retorna os resultados à interface.
   xiii. **Exibir Resultados:** A interface exibe os resultados das coleções de imagens ao usuário.
3. **Elementos Relevantes:**
   1. Interface de Pesquisa
   2. Controlador (Flask)
   3. Serviço de Pesquisa
   4. Model (MongoDB)
   5. Cache (Redis)

---

## **Diagrama de Caso de Uso Único (Englobando Todos os Cenários)**

**Instruções para Construção do Diagrama de Caso de Uso Único:**

1. **Identifique os Atorese o Sistema:**
   - Ator Principal: Usuário
   - Sistema: Sua Aplicação
2. **Identifique os Casos de Uso:**
   - Realizar Upload de Arquivo
   - Criar Coleção
   - Visualizar Documento
   - Editar Documento
   - Salvar Edições
   - Definir Acesso
   - Revogar Acesso
   - Selecionar Texto
   - Realizar Tradução
   - Selecionar Documentos
   - Escolher Edições em Lote
   - Aplicar Edições
3. **Descreva as Interações:**
   - Represente cada ator (Usuário) e o sistema (Aplicação) como blocos.
   - Conecte cada ator ao caso de uso correspondente com linhas sólidas.
4. **Identifique os Relacionamentos:**
   - Use linhas de associação para mostrar a relação entre atores e casos de uso.
   - Adicione descrições breves nas linhas para indicar a ação principal do caso de uso.
5. **Adicione Notas (Opcional):**
   - Se necessário, você pode adicionar notas ou descrições adicionais nos casos de uso para detalhar a interação.

---

## **Identificando os Relacionamentos:**

1. **Realizar Upload de Arquivo**
   - **Estende:** Criar coleção (Se o usuário não tiver nenhuma coleção criada)
2. **Criar Coleção**
3. **Visualizar Documento**
   - **Estende:** Editar Documento (Se o usuário escolher editar o documento após a visualização)
   - **Estende:** Realizar Tradução (Se o usuário escolher traduzir o texto após selecioná-lo)
4. **Editar Documento**
   - **Inclui:** Aplicar Edições (Parte do fluxo de edição)
5. **Definir Acesso**
6. **Revogar Acesso**
7. **Selecionar Texto**
   - **Estende:** Realizar Tradução (Se o usuário escolher traduzir o texto após selecioná-lo)
8. **Realizar Tradução**
   - **Inclui:** Aplicar Edições (Parte do fluxo de tradução)
9. **Selecionar Documentos**
   - **Estende:** Escolher Edições em Lote (Para evitar duplicação de lógica, a etapa de seleção de documentos é incluída no caso de uso de edições em lote)
10. **Escolher Edições em Lote**
11. **Aplicar Edições**

- **Inclui:** Selecionar Documentos (Parte do fluxo de aplicação de edições)

**Descrição do Diagrama de Caso de Uso:**

O diagrama de caso de uso apresenta os principais cenários funcionais da aplicação. O ator principal é o "Usuário", que interage com o "Sistema" representando a sua aplicação. Os casos de uso são representados como elipses e estão conectados por setas que indicam os relacionamentos entre eles.

O sistema é dividido em funcionalidades distintas. O grupo de casos de uso "Gerenciamento de Documentos" inclui ações relacionadas à manipulação de documentos, como upload, edição, visualização, tradução e aplicação de edições em lote. O grupo "Gerenciamento de Acesso" envolve ações de controle de permissões de acesso às funcionalidades.

O diagrama mostra os relacionamentos de extensão e inclusão entre os casos de uso. As extensões indicam que um caso de uso pode estender outro caso de uso em cenários específicos. As inclusões mostram que um caso de uso inclui outro caso de uso para reutilização de funcionalidades comuns.

O caso de uso "Visualizar Documento" estende os casos de uso "Editar Documento" e "Realizar Tradução" para cenários em que o usuário deseja editar o documento após a visualização ou traduzir o texto após a seleção. O caso de uso "Realizar Tradução" inclui o caso de uso "Salvar Edições" para garantir que as edições sejam salvas durante a tradução.

Da mesma forma, o caso de uso "Selecionar Texto" estende o caso de uso "Realizar Tradução" para permitir que o usuário escolha traduzir o texto selecionado. O caso de uso "Selecionar Documentos" estende o caso de uso "Escolher Edições em Lote" para evitar duplicação de lógica na seleção de documentos.

O caso de uso "Aplicar Edições" inclui o caso de uso "Selecionar Documentos" como parte do fluxo de aplicação de edições em lote. Essa estrutura de relacionamentos ajuda a organizar e reutilizar a lógica dos casos de uso, proporcionando uma visão abrangente das interações da aplicação com o usuário.
