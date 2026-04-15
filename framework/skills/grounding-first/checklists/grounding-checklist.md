# Checklist de Grounding

Antes de entregar qualquer código ou afirmação factual, responda cada item com evidência:

- [ ] Eu li literalmente a solicitação do usuário e listei os termos ambíguos.
- [ ] Cada termo ambíguo foi resolvido por pergunta ao usuário ou por referência explícita.
- [ ] Para cada arquivo ou símbolo mencionado na resposta, eu rodei `Read`, `Grep` ou `Glob` e vi o conteúdo real.
- [ ] Para cada API de biblioteca ou framework, eu consultei `context7` ou a documentação oficial via `WebFetch` na tarefa corrente.
- [ ] Para cada comando proposto, eu verifiquei a sintaxe contra a ferramenta correspondente (`--help`, doc oficial ou execução).
- [ ] Nenhuma afirmação confiante foi feita sem citação (`arquivo:linha`, URL, ou quote do usuário).
- [ ] Incertezas foram declaradas explicitamente em vez de mascaradas com linguagem segura.
- [ ] Nenhuma inferência depende de outra inferência não verificada.
- [ ] Nenhum import, método ou config foi citado apenas porque "existe em projetos parecidos".
- [ ] Quando o comportamento correto dependeu de uma versão específica, eu verifiquei a versão instalada no repositório.
- [ ] Sou capaz de apontar, para cada decisão de implementação, a fonte que a justifica.

Se qualquer item falhar, pare, verifique ou pergunte. Não entregue.
