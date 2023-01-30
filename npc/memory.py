
from langchain.chains.llm import LLMChain
from typing import Any, Dict, List
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory


def _get_prompt_input_key(inputs: Dict[str, Any], memory_variables: List[str]) -> str:
    # "stop" is a special key that can be passed as input but is not used to
    # format the prompt.
    prompt_input_keys = list(set(inputs).difference(memory_variables + ["stop"]))
    if len(prompt_input_keys) != 1:
        raise ValueError(f"One input key expected got {prompt_input_keys}")
    return prompt_input_keys[0]

class NPCMemory(ConversationSummaryBufferMemory):

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save context from this conversation to buffer."""
        if self.input_key is None:
            prompt_input_key = _get_prompt_input_key(inputs, self.memory_variables)
        else:
            prompt_input_key = self.input_key
        if self.output_key == "all":
            outputs['all'] = "\n".join([f"{k.capitalize()}: {v}" for k, v in outputs.items()])
        if self.output_key is None:
            if len(outputs) != 1:
                raise ValueError(f"One output key expected, got {outputs.keys()}")
            output_key = list(outputs.keys())[0]
        else:
            output_key = self.output_key
        human = f"{self.human_prefix}: {inputs[prompt_input_key]}"
        ai = f"{self.ai_prefix}: {outputs[output_key]}"
        new_lines = "\n".join([human, ai])
        self.buffer.append(new_lines)
        # Prune buffer if it exceeds max token limit
        curr_buffer_length = sum(self.get_num_tokens_list(self.buffer))
        if curr_buffer_length > self.max_token_limit:
            pruned_memory = []
            while curr_buffer_length > self.max_token_limit:
                pruned_memory.append(self.buffer.pop(0))
                curr_buffer_length = sum(self.get_num_tokens_list(self.buffer))

            chain = LLMChain(llm=self.llm, prompt=self.prompt)
            self.moving_summary_buffer = chain.predict(
                summary=self.moving_summary_buffer, new_lines=("\n".join(pruned_memory))
            )