#!/usr/bin/env python
import sys

from candid_ai.crew import CandidAICrew

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'cv_file': './data/cv.pdf',
        'linkedin_url': 'https://www.linkedin.com/in/denis-hugo-perafan-b0210567/',
        'job_description': './data/job_description.txt'
    }
    CandidAICrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'cv_file': './data/cv.pdf',
        'linkedin_url': 'https://www.linkedin.com/in/denis-hugo-perafan-b0210567/',
        'job_description': './data/job_description.txt'
    }
    try:
        CandidAICrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CandidAICrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'cv_file': './data/cv.pdf',
        'linkedin_url': 'https://www.linkedin.com/in/denis-hugo-perafan-b0210567/',
        'job_description': './data/job_description.txt'
    }
    try:
        CandidAICrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
