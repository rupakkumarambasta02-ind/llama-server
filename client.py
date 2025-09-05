from openai import OpenAI
import requests 
from langchain.prompts import PromptTemplate

from contextlib import contextmanager
from typing import Iterator, List
import time

@contextmanager
def timer() -> Iterator[List[float]]:
    """Context manager that yields (start, end) timestamps."""
    t = [time.perf_counter()]   # mutable list
    yield t
    t.append(time.perf_counter())
question = """
Co) Mi be 1 @ act) Bs coec 1@ ev YG Nod JF AA IO Hom JO oo: (GF use (1 orn f] IF oo FO sce (OD x | © new + - o x
€ 9 G hackerrank.com/challenges/non-divisible-subset/problem?isFullScreen=true bxd 6) e 2 © O | Cr)
Bo | © Office Bookmarks (9 crick (9 Insight (CO Al @ Online Courses-te.. BS Home-MicrosoftA.. CQ gen % IBP-GDO-Activity.. (9 af | © AllBookmarks
HackerRanki Ill Propare by Algorithms}og Implementation Jpg Non: Divisible Subset Exit Full Screen View Ma‘

aa a
Given a set of distinct integers, print the size of a maximal subset of 5 Change Theme Language} Pypy 3 ¥ © H
€ where the sum of any 2 numbers in S" is not evenly divisible by k. ~
Ss 1 #!/bin/python3
rs Example 2
a S = (19,10, 12, 10, 24, 25, 22] k= 4 3 import math
4 ‘import os
One of the arrays that can be created is 5’[0) = [10, 12, 25]. Another S import random
. is S’[1] = [19, 22, 24]. After testing all permutations, the maximum & ‘import re
7 import sys
length solution array has 3 elements. 8
é Function Description 2 o #
a F3 10 # Complete the 'nonDivisibleSubset' function below.
is Complete the nonDivisibteSubset function in the editor below. 11 #
é a . 12. # The function is expected to return an INTEGER.
nonDivisibleSubset has the following parameter(s): 13 # The function accepts following parameters:
* int Sin]: an array of integers 14 # 1. INTEGER k
—_— ; S 15  # 2. INTEGER_ARRAY s
© int k: the divisor
16 # —
Returns Line: 37 Col: 1
2
8 * int: the length of the longest subset of S meeting the criteria
a
3 Input Format (CD) Test against custom input Runcefergy KOACGOS)
> vy v
™)
: on rs , @ @ & ) ENG a uy 1824
& oo QeEe*eaeo e (@| a BN Pana @ ke A 2B iy FE 708-2025
                        """

class LLM:
    def __init__(self):
        self.api_url = "http://localhost:8000/openai/v1/chat/completions"
        self.api_key = "key"

    def call_with_prompt(self,question):
        try:
            language = "Python"
            prompt = PromptTemplate(
                input_variables=["question", "language"],
                template=(
                    "You are given a transcript extracted from an audio recording. "
                    "This transcript may contain irrelevant discussion or non-technical content.\n\n "
                    "Your task is to:\n"
                    "1. Identify and extract the most relevant technical question from the transcript below.\n"
                    "2. Determine whether the question is theoretical(e.g., concept explanation) or practical (e.g., requires code).\n"
                    "3. If theoretical, provide a clear and concise explanation.\n" 
                    "4. If practical, provide a concise, correct code solution in {language}.\n"
                    "If no language is mentioned or it's unclear, default to Python.\n\n"
                    "Transcript:\n{question}\n\n"
                    "Respond in the following format:\n"
                    "Question: <extracted question>\n"
                    "Answer:\n```{language}\n<code here>\n```"
                )
            )
            with timer() as t:
                response = self._call(prompt.format(question=question, language=language))
            llm_response_time = (t[1] - t[0]) * 1000
            print(f"llm_reponse_time {llm_response_time}")
            print(f"Response: recvd...", response)
            return f"{response}"
        except Exception as e:
            print(f"LLM Response failed: {str(e)}")
            raise Exception(f"LLM Response failed: {str(e)}")

    def _call(self,prompt: str, stop=None) -> str:
        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "codellama:7b",  # Valid Groq model
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 500,
                    "temperature": 0.7,  # Valid float32 value
                    "n": 1  # Must be 1 for Groq
                }
            )
            response.raise_for_status()  # Raises exception for 4xx/5xx errors
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as e:
            error_message = f"HTTP Error: {e.response.status_code} - {e.response.text}"
            raise Exception(error_message)
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")
        
if __name__ == "__main__":
    llm = LLM()
    llm.call_with_prompt(question)
