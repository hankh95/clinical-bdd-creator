# Santiago: Four-Layer Model Lessons Learned

## Four-Layer Architecture for Clinical Knowledge Processing

The Santiago service implements a four-layer model for processing clinical guidelines and knowledge:

1. **Layer 1: Raw Text Processing**
   - Input: Clinical guideline documents (PDFs, text)
   - Processing: NLP extraction, entity recognition, relationship identification
   - Output: Structured text with identified clinical concepts

2. **Layer 2: Structured Knowledge Representation**
   - Input: Processed clinical concepts from Layer 1
   - Processing: Ontology mapping, taxonomy classification, knowledge graph construction
   - Output: Structured clinical knowledge in graph format

3. **Layer 3: Computable Logic and Rules**
   - Input: Structured knowledge from Layer 2
   - Processing: Rule extraction, logic formalization, decision criteria definition
   - Output: Executable clinical logic and decision rules

4. **Layer 4: Executable Workflows and Actions**
   - Input: Computable logic from Layer 3
   - Processing: Workflow orchestration, action sequencing, outcome generation
   - Output: Executable clinical workflows and recommendations

## Four-Layer Model Evolution

| Layer | Version 01 (Current Implementation) | Version 02 (NeuroSymbolic Enhancement) |
|-------|-------------------------------------|----------------------------------------|
| **Layer 0: Raw Text** | PDF, HTML or text files | Indexed text, tables, figures, references to support deep asset linking |
| **Layer 1: Raw Text** | Basic NLP extraction, entity recognition | Neural NLP with clinical language models, advanced entity disambiguation |
| **Layer 2: Structured Knowledge** | Simple ontology mapping, basic graph construction | NeuroSymbolic knowledge graphs with embeddings, symbolic reasoning over graphs |
| **Layer 3: Computable Logic** | Rule-based logic extraction, basic decision trees | Hybrid neural-symbolic reasoning, probabilistic logic, uncertainty handling |
| **Layer 4: Executable Workflows** | Sequential workflow execution, basic orchestration | Dynamic workflow generation, multi-path reasoning, adaptive execution |

## Lessons Learned from Version 01 - includes some proposed improvements

We learned that we need to load the original knowledge document and create a layer 0 in the graph to support deep asset linking from all of the other layers. We should be able to trace back any asset, logic, decision table, workflow back to the text. There is a TOC file we will add to show one approach - be sure to create a gh issue to find and incorporate this. 

Layer 1 - We learned there are a core set of valuable semantic relationships that are the most important for reasoning. drug x TREATS condition Y - We will need to upload the last set and expand to cover 
- treats
- investigates
- complicates
- risk-factor
Most of these and the rest of a "core canonical list" we can derive from an analysis of SNOMED core relationships, FHIR-CPG core relationships, OpenEHR Architype relationships and properties and our core usage scenarios for real use in decision making. In addition to the core list, every guideline and specialty will have extended relationships - however, we try to limit to those that are involved in actual decision making - Called FACTS THAT MATTER. 

Layer 2 should include the UMLS ontologies such as SNOMED, LOINC, RxNorm, ICD-10 and others loaded into the graph with unique ID's. We learned that using a separate terminology server like OntoServer creates too much delay during reasoning which is required to be near real time at scale (as doctors and care teams don't wait.

Layer 2 should include value sets from sources like VSAC and these can be pulled in for the vasc website as the knowledge is built and we need value sets in layer 2 and 3. Many of these can be found on grokipedia or wikipedia.

Layer 3 - For the prior version, this was built from the layer 2 triples (of pre-identified FHIR-CPG assets and built almost entirely in FHIR-CPG. I suggest we also incorporate ideas from OpenEHR architypes and have the ability to load both or multiple models. One key lesson learned is that the closer we can represent a concept to the way it reads in the guideline and stored as one asset the better. One example is if we extracting/asset building the NCCN guideline and in a treatment decision the TNM grading scale is needed - then we should build this decision table as one complete asset that has all of the concepts and logic needed to calculate it's values. FHIR-CPG would move the logic out to a library file - that is NOT good as we want this asset/object to have it's logic stored with it and in it's native format (decision table). The same can be said of figures that are decision trees, workflows, sequences, triggers. 
Layer 3 - should be adapted for Neurosymbolic reasoning, but we MUST be able to trace every decision back to it's source in a guideline/ study and prove the decision and reasoning matches the text. This is why the BDD test framework is the key part of the architecture to start on. In addition to trying to prove the fidelity of the derives graph assets, the clinical knowledge author will want to be able to run what-if scenarios on a guideline and we may build automation to help with tasks E.g. 1. Review this new publication and describe how it changes current practice and what assets would change and what decisions would be affected. 2. A new guideline udpate is published, review the list of changes and create a set of review tasks of all the changes for a human author to approve before making the changes and BDD tests that validate the changes. 

Layer 4 - We have learned that separating time and large grained sequencing seems like a good concept but has not been tested. Most of the usage scenarios take place in real time, but many need to be driven by time elapsed, scheduled activities (labs every 6 mo) and conditional branching based on time series of data (lab value increasing at a certain rate)

Additional Lessons
A. We have had the most success representing a guidelines knowledge assets in git and using github and modern agile software development (TDD, BDD) applied to clinical knowledge (clinical-knowledge-ops) to create, update and publish knowledge. The main requirement is versioning of knowledge but all of the principles in devops and lean-agile development apply as well. HOWEVER, we may want to research manageing the knowledge lifecycle in the graph and even if we don't, the authoring tools will use the live knowledge graph extensively for authoring tasks. 
B. Guidelines are not always accurate or kept up to date by the organizations themselves. We may want to consider ingesting the clinical studies themselves and using EBMonFHIR - as this is a deep model for all of the data and conclusions of studies. 
C. Multiple approaches to validation - testing lots of clinical scenarios requires that we validate the expected answer for a scenario. One approach I have used is to pose the clinical BDD scenario to 3-5 different AI models and seeing if we get the same expected answer. 
D. Goals and measures can be built from the knowledge at a level not being done today. When guideline changes are made, there is a reason that should relate to a new goal and measure. Did the change or referenced study show a reduction in certain adverse events related to the new recommendation? We should build these goals and keep them tied to the decisions so we and our consuming partners can easily measure the clinical imrpovement of higher adhereance to guidelines. 
E. There are three key aspects to measuring CDS and effectiveness of our knowledge system. 1. Did the intervention follow the 5 rights of CDS and did it get used. 2. Was the recommedation followed. 3. If the recommendation was followed, did we see a measurable clinical improvement. Collecting data on this combination allows us to improve 1. the CDS tool/method of intervention (behavior change) 2. the clinical effect of following the guideline (concordance) - 3. The knowledge feedback loop to the guideline org (where are guidelines being followed and where not. Where are there gaps?


## Proposed Improvements for Version 02

Proposed improvements inline above with the lessons. We should keep an active research and conclusions folder and use as much of Jeff Goethelf's Lean Hypothysis testing to create, review, and test core technical / business / user hypotheses and measure. 

---
*Document Version: 2.0*
*Last Updated: November 2025*
*Focus: Four-Layer Model Evolution*
