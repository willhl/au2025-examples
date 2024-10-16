
# AU2024 Examples

This reposity contains example Python code demonstrated at my AU 2024 talk on Event Driven design.

It consists of Python code for: 
 - Microsoft authenticaion service client (MSAL)
 - GraphQL client
 - Two example design behaviour services which use GraphQL subscriptions to respond to changes in the design.

To use the examples, you'll first need to start a `neo4j/GraphQL` API with the required schema (details comming soon).

Once the GraphQL API is running, seed to DB with a project and the required types:

#### Create a Project
Query
```
mutation CreateProjects {
createProjects(
    input: [{ Name: "AU2024 Example Project", Project_Code: "SAMPLE" }]
) {
    projects {
    Id
    }
}
}
```

#### Create the example equipment types
Query
```
mutation CreateElectricalTypes($projectCode: String) {
createElectricalOutletTypes(
    input: [
    {
        Name: "230v Single Socket Non Essential"
        NumberOfOutlets: 1
        Project: { connect: { where: { node: { Project_Code: $projectCode } } } }
    }
    {
        Name: "230v Double Socket Non Essential"
        NumberOfOutlets: 2
        Project: { connect: { where: { node: { Project_Code: $projectCode } } } }
    }
    {
        Name: "230v Cleaners Socket"
        NumberOfOutlets: 1
        Project: { connect: { where: { node: { Project_Code: $projectCode } } } }
    }
    {
        Name: "230v Fused Connection Unit"
        NumberOfOutlets: 1
        Project: { connect: { where: { node: { Project_Code: $projectCode } } } }
    }
    ]
) {
    electricalOutletTypes {
    Id
    Name
    }
}
createMvhrUnitTypes(
    input: [
    {
        Name: "MVHR Generic"
        Project: { connect: { where: { node: { Project_Code: "SAMPLE" } } } }
    }
    ]
) {
    info {
    nodesCreated
    }
}
}
```

Variables
```
{
"projectCode" :"SAMPLE"
}
```

### To start the behaviour services
```
cd Python
pip install -r requirements.txt
py StartBehaviours.py
```