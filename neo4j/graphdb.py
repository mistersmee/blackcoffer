"""
Copyright (C) 2025 Aseem Athale

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from neo4j import GraphDatabase

# Connect to Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

# Create the Knowledge Graph
def create_graph(tx):
    tx.run("""
    // Create Institutions
    MERGE (uni1:Institution {name: 'MIT', location: 'USA'})
    MERGE (uni2:Institution {name: 'Stanford', location: 'USA'})
    MERGE (uni3:Institution {name: 'Oxford', location: 'UK'})

    // Create Authors
    MERGE (alice:Author {name: 'Alice Smith'})
    MERGE (bob:Author {name: 'Bob Johnson'})
    MERGE (charlie:Author {name: 'Charlie Brown'})

    // Link Authors to Institutions
    MERGE (alice)-[:AFFILIATED_WITH]->(uni1)
    MERGE (bob)-[:AFFILIATED_WITH]->(uni2)
    MERGE (charlie)-[:AFFILIATED_WITH]->(uni3)

    // Create Papers
    MERGE (paper1:Paper {title: 'Graph Databases 101', year: 2022, abstract: 'Introduction to graph databases'})
    MERGE (paper2:Paper {title: 'Advanced Graph Algorithms', year: 2023, abstract: 'Exploring advanced graph algorithms'})
    MERGE (paper3:Paper {title: 'Knowledge Graphs in AI', year: 2024, abstract: 'Using knowledge graphs for AI applications'})

    // Link Papers to Authors
    MERGE (paper1)-[:AUTHORED_BY]->(alice)
    MERGE (paper2)-[:AUTHORED_BY]->(bob)
    MERGE (paper3)-[:AUTHORED_BY]->(charlie)

    // Create Keywords
    MERGE (kg:Keyword {term: 'Knowledge Graphs'})
    MERGE (ai:Keyword {term: 'Artificial Intelligence'})
    MERGE (algo:Keyword {term: 'Algorithms'})

    // Link Papers to Keywords
    MERGE (paper1)-[:HAS_KEYWORD]->(kg)
    MERGE (paper2)-[:HAS_KEYWORD]->(algo)
    MERGE (paper3)-[:HAS_KEYWORD]->(kg)
    MERGE (paper3)-[:HAS_KEYWORD]->(ai)

    // Citation Links
    MERGE (paper3)-[:CITED]->(paper1)
    MERGE (paper3)-[:CITED]->(paper2)
    """)

# Add a new paper dynamically
def add_paper(tx, title, year, abstract, authors, keywords, citations):
    # Create Paper
    tx.run("MERGE (p:Paper {title: $title, year: $year, abstract: $abstract})",
           title=title, year=year, abstract=abstract)

    # Link Authors
    for author_name, institution in authors:
        tx.run("""
        MERGE (a:Author {name: $author_name})
        MERGE (i:Institution {name: $institution})
        MERGE (a)-[:AFFILIATED_WITH]->(i)
        WITH a
        MATCH (p:Paper {title: $title})
        MERGE (p)-[:AUTHORED_BY]->(a)
        """, title=title, author_name=author_name, institution=institution)

    # Link Keywords
    for keyword in keywords:
        tx.run("""
        MERGE (k:Keyword {term: $keyword})
        WITH k
        MATCH (p:Paper {title: $title})
        MERGE (p)-[:HAS_KEYWORD]->(k)
        """, title=title, keyword=keyword)

    # Link Citations
    for cited_title in citations:
        tx.run("""
        MATCH (p:Paper {title: $title})
        MATCH (cited:Paper {title: $cited_title})
        MERGE (p)-[:CITED]->(cited)
        """, title=title, cited_title=cited_title)

# Query: Find co-authorship networks
def co_authors(tx, author_name):
    result = tx.run("""
    MATCH (a:Author {name: $author_name})-[:AUTHORED_BY]-(p:Paper)-[:AUTHORED_BY]-(coauthor:Author)
    RETURN DISTINCT coauthor.name AS CoAuthor
    """, author_name=author_name)
    return [record["CoAuthor"] for record in result]

# Query: Discover most-cited papers
def most_cited_papers(tx, limit=5):
    result = tx.run("""
    MATCH (p:Paper)<-[c:CITED]-()
    RETURN p.title AS Paper, COUNT(c) AS Citations
    ORDER BY Citations DESC
    LIMIT $limit
    """, limit=limit)
    return [(record["Paper"], record["Citations"]) for record in result]

# Query: Identify top research areas
def top_keywords(tx, limit=5):
    result = tx.run("""
    MATCH (p:Paper)-[:HAS_KEYWORD]->(k:Keyword)
    RETURN k.term AS Keyword, COUNT(p) AS Frequency
    ORDER BY Frequency DESC
    LIMIT $limit
    """, limit=limit)
    return [(record["Keyword"], record["Frequency"]) for record in result]

# Query: Trace citation lineage
def citation_lineage(tx, paper_title):
    result = tx.run("""
    MATCH path = (p:Paper {title: $paper_title})-[:CITED*]->(cited:Paper)
    RETURN nodes(path) AS Lineage
    """, paper_title=paper_title)
    return [[node["title"] for node in record["Lineage"]] for record in result]

# Initialize the Graph
with driver.session() as session:
    session.execute_write(create_graph)
    print("Knowledge Graph created successfully.")

    # Add a new research paper
    session.execute_write(add_paper,
        title="Graph Neural Networks",
        year=2025,
        abstract="Exploring the intersection of graphs and neural networks",
        authors=[("Eve Adams", "MIT"), ("Frank White", "Oxford")],
        keywords=["Graph Neural Networks", "Deep Learning"],
        citations=["Graph Databases 101", "Advanced Graph Algorithms"]
    )
    print("New paper added successfully.")

    # Execute advanced queries
    print("Co-authors of 'Alice Smith':", session.execute_read(co_authors, "Alice Smith"))
    print("Most-cited papers:", session.execute_read(most_cited_papers))
    print("Top research areas:", session.execute_read(top_keywords))
    print("Citation lineage for 'Graph Neural Networks':", session.execute_read(citation_lineage, "Graph Neural Networks"))

driver.close()
