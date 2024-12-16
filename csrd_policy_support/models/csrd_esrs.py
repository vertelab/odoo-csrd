from odoo import models, fields, api, _

import logging, os
import markdown
from odoo.exceptions import ValidationError

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser

_logger = logging.getLogger(__name__)


class DocumentCSRD(models.Model):
    _inherit = 'csrd.esrs'

    ai_question = fields.Html()

    def ai_templet_prompt(self):

        system_prompt = \
            _("""
        {context}

        ---

        The context above is a description and summary of a company. And below is an ESRS datapoint requirement. 
        Below the ESRS datapoint requirement, there is a user question. With the user question and the ESRS datapoint 
        requirement in mind, create an ESRS policy that is relevant for the business/company.

        ---
        
        {document}

        ---

        {question}

        ---
        Answer: 
        """).strip()

        return PromptTemplate(template=system_prompt, input_variables=["context", "document", "question"])

    def create_ai_policy(self):
        for rec in self:
            company_id = rec.company_id

            if company_id.ai_company_context:
                ai_message = self.ai_templet_prompt().invoke(
                    {"context": company_id.ai_company_context, "document": rec.csrd_name, "question": self.ai_question})
                ai_answer = self.get_llm(company_id=company_id).invoke(ai_message)
                parser = StrOutputParser()
                _logger.error(f"{ai_answer=}")
                rec.write({'description': markdown.markdown(parser.invoke(ai_answer))})

    def get_llm(self, company_id):

        if not company_id.ai_api_key:
            raise ValidationError(_("Please add a api key for your llm."))

        if company_id.ai_model == "chatgpt":

            os.environ["OPENAI_API_KEY"] = company_id.ai_api_key
            return ChatOpenAI(model="gpt-4o")

        elif company_id.ai_model == "mistral":

            os.environ["MISTRAL_API_KEY"] = company_id.ai_api_key
            return ChatMistralAI(model="mistral-large-latest")

        else:
            raise ValidationError(_("Please select a llm on your company."))
