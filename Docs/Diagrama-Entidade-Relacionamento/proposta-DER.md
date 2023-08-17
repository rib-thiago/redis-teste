# Proposta Construção de DER

**Instruções e Identificação:**

1. **Entidades:**
   - **User:** Representa os usuários do sistema, com informações como nome, email e nível de acesso.
   - **Collection:** Representa as coleções de imagens ou documentos históricos criadas por usuários, com atributos como título e descrição.
   - **Image/Document:** Representa as imagens ou documentos carregados pelos usuários, com metadados relevantes.
   - **CacheItem:** Representa os itens armazenados no Redis para caching, como consultas frequentes.
2. **Relacionamentos:**
   - Um usuário pode criar várias coleções (1:N).
   - Uma coleção pertence a um usuário (N:1).
   - Uma coleção pode conter várias imagens ou documentos (1:N).
   - Uma imagem ou documento pertence a uma coleção (N:1).
   - O cache pode armazenar várias entradas de dados (1:N).

**Construção do DER:**

1. Desenhe retângulos para cada entidade identificada: User, Collection, Image/Document e CacheItem.
2. Conecte esses retângulos com linhas para representar os relacionamentos. Use linhas com setas indicando a direção do relacionamento.
3. Adicione os atributos importantes de cada entidade dentro dos retângulos.
4. Se necessário, adicione anotações ou descrições para esclarecer aspectos específicos dos relacionamentos ou entidades.
5. Certifique-se de destacar os relacionamentos 1:N e N:1.

Lembrando que, devido à abordagem híbrida, algumas informações podem ser armazenadas no MongoDB (estruturadas) e outras no Redis (dados de cache). O DER representa a estrutura lógica das entidades e seus relacionamentos, independente da forma como esses dados são armazenados fisicamente nos bancos de dados.
