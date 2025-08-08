from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from src.stock_analyst_01.tools.custom_tool import SearchScreanerTool, GetStockDetailsFromScreanerTool, GetPeersDataFromScreanerTool, GetNewsDataFromScreanerTool
# from src.stock_analyst_01.tools.custom_tool import SearchScreanerTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class StockAnalyst01():
    """StockAnalyst01 crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def stock_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['stock_researcher'], # type: ignore[index]
            # verbose=True,
            tools=[SearchScreanerTool(), GetStockDetailsFromScreanerTool(), GetPeersDataFromScreanerTool(), GetNewsDataFromScreanerTool()]
            
        )

    @agent
    def sentiment_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['sentiment_analyst'], # type: ignore[index]
            verbose=True
        )

    @agent
    def stock_quantitative_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['stock_quantitative_analyst'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def stock_report_summariser(self) -> Agent:
        return Agent(
            config=self.agents_config['stock_report_summariser'], # type: ignore[index]
            verbose=True
        )
    
    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def define_stock_to_analyze(self) -> Task:
        return Task(
            config=self.tasks_config['define_stock_to_analyze'], # type: ignore[index]\
            output_variable = "stock_details"
        )

    @task
    def gather_stock_data(self) -> Task:
        return Task(
            config=self.tasks_config['gather_stock_data'], # type: ignore[index]
        )

    @task
    def perform_sentiment_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['perform_sentiment_analysis'], # type: ignore[index]
        )

    @task
    def perform_quantitative_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['perform_quantitative_analysis'], # type: ignore[index]
        )
    
    @task   
    def compile_final_report(self) -> Task:
        return Task(
            config=self.tasks_config['compile_final_report'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StockAnalyst01 crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            sequential=True,
            max_rpm=1,
            output_file="output.md",
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
