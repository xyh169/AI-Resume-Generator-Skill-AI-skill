# Domain And Role Seed Examples

Use this reference only as a seed for role/domain tagging and resume language. Always prefer the user's real JD, current company posting, and candidate-provided evidence.

## Research Grounding

- Product management language should emphasize vision, goals, roadmap, backlog, metrics, stakeholder alignment, and prioritization.
- AI Agent engineering language should emphasize LLM application architecture, RAG, tool calling, memory/state, evaluation, tracing, reliability, safety, and deployment.
- Healthcare language should emphasize workflow, patient/provider experience, interoperability, EHR/EMR, HL7/FHIR, privacy, evidence, and operational safety.
- Finance language should emphasize risk, controls, fraud, KYC/AML, model governance, auditability, compliance, market integrity, and measurable business outcomes.

## Role Target Profiles

| Target | Primary signals | Secondary signals |
|---|---|---|
| Product Manager - Healthcare | clinical workflow, patient/provider experience, roadmap, PRD, stakeholder alignment, FHIR/EHR, adoption metrics | privacy, care coordination, analytics dashboard, operational efficiency |
| Product Manager - Finance | fintech product, payments, lending, risk, KYC/AML, fraud, compliance, revenue metrics, backlog prioritization | audit trail, data product, customer onboarding, churn, NPS |
| AI Agent Engineer - Healthcare | LLM agents, RAG over clinical/operational knowledge, FHIR/API tools, PHI-safe workflow, evals, observability | guardrails, human review, latency, audit logs, retrieval quality |
| AI Agent Engineer - Finance | agentic RAG, compliance assistant, fraud/risk workflows, tool permissions, model risk controls, evals, traceability | KYC/AML, surveillance, backtesting, data lineage, secure deployment |

## Keyword Seeds

### Product Manager - Healthcare

Use when the candidate has evidence:

```text
roadmap, PRD, backlog, user research, clinician interview, patient journey,
provider workflow, EHR, EMR, HL7, FHIR, interoperability, care coordination,
clinical operations, adoption, activation, retention, NPS, workflow efficiency,
privacy, regulated product, cross-functional delivery
```

Do not use unless evidenced:

```text
HIPAA ownership, FDA submission, clinical validation, medical device compliance,
FHIR implementation, EHR integration
```

### Product Manager - Finance

Use when the candidate has evidence:

```text
fintech, payments, lending, credit risk, fraud prevention, KYC, AML,
customer onboarding, transaction monitoring, compliance workflow, risk controls,
data dashboard, experimentation, conversion, revenue, retention, churn, NPS,
stakeholder alignment, roadmap, PRD, go-to-market
```

Do not use unless evidenced:

```text
SEC/FINRA compliance ownership, model risk governance, trading surveillance,
AML program ownership, regulatory reporting sign-off
```

### AI Agent Engineer - Healthcare

Use when the candidate has evidence:

```text
LLM application, AI agent, agent orchestration, RAG, vector search,
tool calling, function calling, workflow automation, FHIR API, EHR data,
retrieval evaluation, hallucination mitigation, PHI redaction, audit log,
human-in-the-loop, prompt evaluation, tracing, latency, reliability, deployment
```

Do not use unless evidenced:

```text
clinical decision support, diagnosis automation, HIPAA compliance lead,
production PHI processing, FDA-regulated AI system
```

### AI Agent Engineer - Finance

Use when the candidate has evidence:

```text
LLM agent, agentic RAG, compliance assistant, risk analysis, fraud workflow,
KYC/AML document review, tool permissioning, retrieval grounding, eval suite,
model monitoring, audit trail, data lineage, secure API integration,
policy guardrails, human approval, latency, cost optimization
```

Do not use unless evidenced:

```text
approved investment advice, autonomous trading, regulatory reporting owner,
model validation sign-off, SEC/FINRA rule interpretation authority
```

## Candidate Fact Examples

These are examples of structure and wording only. Replace all content with user-supported facts.

### Product Manager - Healthcare Fact

```json
{
  "id": "fact_pm_healthcare_001",
  "fact_type": "project",
  "title": "Outpatient workflow analytics dashboard",
  "role": "Product Manager",
  "summary": "Defined dashboard requirements for outpatient operations analytics.",
  "actions": ["Interviewed clinicians", "Prioritized backlog", "Coordinated data and engineering delivery"],
  "outcomes": ["Improved visibility into appointment bottlenecks"],
  "skills": ["user research", "PRD", "roadmap", "KPI dashboard"],
  "technologies": ["SQL", "BI", "FHIR"],
  "role_targets": ["product-manager"],
  "domain_tags": ["healthcare", "clinical-workflow", "analytics"],
  "source_ref": {"source_file": "raw_content.md", "source_quote": "replace_with_user_source"},
  "evidence_strength": "medium",
  "verification_status": "needs_metric_confirmation",
  "embedding_text": "Product Manager healthcare clinical workflow dashboard PRD user research KPI FHIR backlog"
}
```

Possible resume bullet:

```markdown
- 围绕门诊运营分析场景，访谈临床与运营角色，沉淀 KPI 口径、PRD 与迭代 backlog，推动数据与工程团队交付可视化看板，提升预约瓶颈识别效率。
```

### Product Manager - Finance Fact

```json
{
  "id": "fact_pm_finance_001",
  "fact_type": "project",
  "title": "Risk onboarding workflow",
  "role": "Product Manager",
  "summary": "Optimized onboarding and risk review workflow for a fintech product.",
  "actions": ["Mapped onboarding funnel", "Defined risk review states", "Coordinated compliance and engineering stakeholders"],
  "outcomes": ["Reduced manual handoff ambiguity"],
  "skills": ["funnel analysis", "PRD", "risk control", "stakeholder management"],
  "technologies": ["SQL", "workflow engine"],
  "role_targets": ["product-manager"],
  "domain_tags": ["finance", "risk", "onboarding"],
  "source_ref": {"source_file": "raw_content.md", "source_quote": "replace_with_user_source"},
  "evidence_strength": "medium",
  "verification_status": "needs_metric_confirmation",
  "embedding_text": "Product Manager fintech onboarding KYC AML risk control PRD funnel compliance stakeholder"
}
```

Possible resume bullet:

```markdown
- 梳理金融产品开户与风控审核链路，定义状态流转、异常分流与埋点口径，协同合规、风控和工程团队收敛 PRD，降低人工交接歧义。
```

### AI Agent Engineer - Healthcare Fact

```json
{
  "id": "fact_agent_healthcare_001",
  "fact_type": "project",
  "title": "Clinical knowledge retrieval assistant",
  "role": "AI Agent Engineer",
  "summary": "Built a retrieval-grounded assistant over healthcare operation documents.",
  "actions": ["Designed RAG pipeline", "Added tool-call guardrails", "Built evaluation set"],
  "outcomes": ["Improved answer grounding and reviewability"],
  "skills": ["RAG", "tool calling", "evaluation", "observability"],
  "technologies": ["Python", "vector database", "LLM API", "FHIR API"],
  "role_targets": ["ai-agent-engineer"],
  "domain_tags": ["healthcare", "agentic-rag", "retrieval"],
  "source_ref": {"source_file": "raw_content.md", "source_quote": "replace_with_user_source"},
  "evidence_strength": "medium",
  "verification_status": "needs_confirmation",
  "embedding_text": "AI Agent Engineer healthcare RAG tool calling FHIR API evaluation tracing audit human review"
}
```

Possible resume bullet:

```markdown
- 构建面向医疗运营知识的 RAG 助手，设计检索分块、工具调用边界与评测集，结合 trace 与人工复核机制提升回答可追溯性，避免将未验证内容写入业务结论。
```

### AI Agent Engineer - Finance Fact

```json
{
  "id": "fact_agent_finance_001",
  "fact_type": "project",
  "title": "Compliance document review agent",
  "role": "AI Agent Engineer",
  "summary": "Developed an agentic workflow for finance compliance document review.",
  "actions": ["Implemented hybrid retrieval", "Restricted tool permissions", "Logged evidence for review"],
  "outcomes": ["Improved review traceability"],
  "skills": ["agentic RAG", "hybrid retrieval", "guardrails", "audit logging"],
  "technologies": ["Python", "LLM API", "vector search", "workflow orchestration"],
  "role_targets": ["ai-agent-engineer"],
  "domain_tags": ["finance", "compliance", "risk"],
  "source_ref": {"source_file": "raw_content.md", "source_quote": "replace_with_user_source"},
  "evidence_strength": "medium",
  "verification_status": "needs_confirmation",
  "embedding_text": "AI Agent Engineer finance compliance agentic RAG hybrid retrieval guardrails audit log model risk"
}
```

Possible resume bullet:

```markdown
- 设计金融合规文档审阅 Agent 流程，结合混合检索、工具权限控制与证据日志，输出可复核的引用链路，支持风控/合规场景下的人工审核闭环。
```

## Gap Questions

Use these questions when the JD asks for a capability but the candidate facts are weak or missing:

| Gap | Ask |
|---|---|
| Healthcare interoperability | 是否做过 HL7/FHIR、EHR/EMR 或医院信息系统接口相关项目？具体负责哪一部分？ |
| Healthcare privacy | 是否处理过 PHI/患者数据、脱敏、权限控制或审计日志？有无可公开描述的边界？ |
| Finance compliance | 是否参与过 KYC/AML、反欺诈、风控审核、监管报送或合规评审流程？ |
| Model/agent evaluation | 是否做过 RAG/Agent 的评测集、失败样本分析、trace、回归测试或线上监控？ |
| Product metrics | 是否有转化率、留存、活跃、NPS、成本、效率、风险命中率等量化结果？ |
| Tool calling | Agent 是否接入过外部 API、数据库、审批系统或业务工具？权限和错误处理怎么设计？ |

## Source Links For Refresh

- Product roadmap and metrics framing: https://assets.productplan.com/content/ProductPlan-Strategic-Roadmap-Planning-Guide.pdf
- OpenAI retrieval/vector store concepts: https://developers.openai.com/api/docs/guides/retrieval
- OpenAI tool use and agent evaluation concepts: https://developers.openai.com/api/docs/guides/tools and https://developers.openai.com/api/docs/guides/agent-evals
- HL7 FHIR healthcare interoperability vocabulary: https://www.hl7.org/fhir/
- FINRA fintech and AI financial services vocabulary: https://www.finra.org/rules-guidance/key-topics/fintech
- Federal Reserve SR 11-7 model risk vocabulary: https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm
