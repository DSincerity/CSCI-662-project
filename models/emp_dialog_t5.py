# coding=utf-8
# copied from bart

import torch
import torch.nn as nn
import torch.nn.functional as F
from models.model_utils import BaseModel
from transformers.generation_utils import top_k_top_p_filtering
from transformers.models.blenderbot_small import (BlenderbotSmallConfig, BlenderbotSmallForConditionalGeneration,)
from transformers import T5ForConditionalGeneration, T5Config, AutoConfig, AutoTokenizer
from transformers.modeling_outputs import (BaseModelOutput, Seq2SeqModelOutput, Seq2SeqLMOutput,)
from .PARAMS import SAMPLE, TEMPERATURE


class Model(BaseModel, T5ForConditionalGeneration):
    def __init__(self, config: T5Config):
        super().__init__(config)

    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        decoder_input_ids=None,
        encoder_outputs=None,
        past_key_values=None,
        labels=None,
        use_cache=None,
        return_dict=None,
        validation=False,
        **kwargs
    ):
        assert self.toker is not None
        # print('input ids: ', input_ids)
        # print(labels)
        # print(kwargs)

        encoded_info = kwargs
        assert (self.training or validation) == (labels is not None), f"train {self.training}: \nlables: {labels}"
        if validation:
            labels[:, 0] = -100

        use_cache = use_cache if use_cache is not None else self.config.use_cache
        if not self.training and not validation: # inference
            use_cache = True
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        outputs = super().forward(
            input_ids,
            attention_mask=attention_mask,
            decoder_input_ids=decoder_input_ids,
            encoder_outputs=encoder_outputs,
            past_key_values=past_key_values,
            use_cache=use_cache,
            return_dict=return_dict,
        )

        lm_logits= outputs.logits
        #loss = outputs.loss

        #print(lm_logits)
        #print(loss)
        #lm_logits = self.lm_head(outputs) #+ self.final_logits_bias

        if validation:
            lm_logits = lm_logits[..., :self.toker.vocab_size].contiguous()

        # if labels is not None:
        #     loss_fct = CrossEntropyLoss(ignore_index=-100)
        #     # move labels to correct device to enable PP
        #     labels = labels.to(lm_logits.device)
        #     loss = loss_fct(lm_logits.view(-1, lm_logits.size(-1)), labels.view(-1))


        masked_lm_loss = None
        if labels is not None:
            loss = F.cross_entropy(lm_logits.view(-1, lm_logits.size(-1)), labels.view(-1), reduction='none')
            loss = loss.view(labels.size(0), labels.size(1))
            label_size = torch.sum(labels.ne(-100), dim=1).type_as(loss)
            masked_lm_loss = torch.sum(loss) / torch.sum(label_size)
            ppl_value = torch.exp(torch.mean(torch.sum(loss, dim=1).float() / label_size.float()))

        if not self.training and not validation: # inference
            if not return_dict:
                output = (lm_logits,) + outputs[1:]
                return ((masked_lm_loss,) + output) if masked_lm_loss is not None else output

            return Seq2SeqLMOutput(
                loss=masked_lm_loss,
                logits=lm_logits,
                past_key_values=outputs.past_key_values,
                decoder_hidden_states=outputs.decoder_hidden_states,
                decoder_attentions=outputs.decoder_attentions,
                cross_attentions=outputs.cross_attentions,
                encoder_last_hidden_state=outputs.encoder_last_hidden_state,
                encoder_hidden_states=outputs.encoder_hidden_states,
                encoder_attentions=outputs.encoder_attentions,
            )

        elif self.training: # training
            assert not validation
            res = {'all': masked_lm_loss, 'ppl': ppl_value, }
            return res

        else: # validation
            assert not self.training
            return loss, label_size

    def predict_strategy(self, logits, data_name, knowledge_name, encoded_info):
        assert not self.training
        strat_id = encoded_info.get('strat_id', None)
        if knowledge_name == 'none':
            if data_name == 'esconv':
                logits = logits[:, 0, -8:]
            elif data_name == 'mi':
                logits = logits[:, 0, -10:]
        elif knowledge_name == 'basic':
            if data_name == 'esconv':
                logits = logits[:, 0, -13:-5]
            elif data_name == 'mi':
                logits = logits[:, 0, -15:-5]
        elif knowledge_name == 'bm25':
            if data_name == 'esconv':
                logits = logits[:, 0, -9:-1]
            elif data_name == 'mi':
                logits = logits[:, 0, -11:-1]
        elif knowledge_name == 'oracle':
            if data_name == 'esconv':
                logits = logits[:, 0, -14:-6]
            elif data_name == 'mi':
                logits = logits[:, 0, -16:-6]
        elif knowledge_name in ['sbert','graph']:
            if data_name == 'esconv':
                logits = logits[:, 0, -16:-8]
            elif data_name == 'mi':
                logits = logits[:, 0, -18:-8]


        if strat_id is not None:
            pred = strat_id
        else:
            if SAMPLE:
                filtered_logits = top_k_top_p_filtering(logits / TEMPERATURE, top_p=0.9)
                pred = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1).squeeze(-1)
            else:
                pred = torch.argmax(logits, dim=-1)

        pred_top1 = torch.topk(logits, k=1, dim=-1)[1]
        pred_top3 = torch.topk(logits, k=3, dim=-1)[1]

        encoded_info.update({
            'pred_strat_id': pred,
            'pred_strat_id_top1': pred_top1,
            'pred_strat_id_top3': pred_top3,
            'pred_strat_id_dist': F.softmax(logits, dim=-1)
        })

    @torch.no_grad()
    def generate(
        self,
        data_name,
        knowledge_name,
        input_ids=None,
        attention_mask=None,
        decoder_input_ids=None,
        return_dict=None,
        **kwargs
    ):
        assert not self.training
        assert self.toker is not None

        encoded_info = kwargs
        assert decoder_input_ids.size(1) == 1
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        encoder_outputs = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask,
            return_dict=return_dict,
        )

        decoder_outputs = self.decoder(
            input_ids=decoder_input_ids,
            encoder_hidden_states=encoder_outputs[0],
            encoder_attention_mask=attention_mask,
            return_dict=return_dict,
        )
        lm_logits = self.lm_head(decoder_outputs.last_hidden_state) #+ self.final_logits_bias
        self.predict_strategy(lm_logits, data_name, knowledge_name, encoded_info)

        if knowledge_name == 'none':
            if data_name == 'esconv':
                decoder_input_ids = torch.cat([decoder_input_ids, encoded_info['pred_strat_id'][..., None] + len(self.toker) - 8], dim=-1)
            elif data_name == 'mi':
                decoder_input_ids = torch.cat([decoder_input_ids, encoded_info['pred_strat_id'][..., None] + len(self.toker) - 10], dim=-1)
        elif knowledge_name == 'basic':
            if data_name == 'esconv':
                decoder_input_ids = torch.cat([decoder_input_ids, encoded_info['pred_strat_id'][..., None] + len(self.toker) - 13], dim=-1)
            elif data_name == 'mi':
                decoder_input_ids = torch.cat([decoder_input_ids, encoded_info['pred_strat_id'][..., None] + len(self.toker) - 15], dim=-1)
        elif knowledge_name == 'bm25':
            if data_name == 'esconv':
                decoder_input_ids = torch.cat([decoder_input_ids, encoded_info['pred_strat_id'][..., None] + len(self.toker) - 9], dim=-1)
            elif data_name == 'mi':
                decoder_input_ids = torch.cat([decoder_input_ids, encoded_info['pred_strat_id'][..., None] + len(self.toker) - 11], dim=-1)
        elif knowledge_name == 'oracle':
            if data_name == 'esconv':
                decoder_input_ids = torch.cat([decoder_input_ids, encoded_info['pred_strat_id'][..., None] + len(self.toker) - 14], dim=-1)
            elif data_name == 'mi':
                decoder_input_ids = torch.cat([decoder_input_ids, encoded_info['pred_strat_id'][..., None] + len(self.toker) - 16], dim=-1)
        elif knowledge_name in ['sbert','graph']:
            if data_name == 'esconv':
                decoder_input_ids = torch.cat([decoder_input_ids, encoded_info['pred_strat_id'][..., None] + len(self.toker) - 16], dim=-1)
            elif data_name == 'mi':
                decoder_input_ids = torch.cat([decoder_input_ids, encoded_info['pred_strat_id'][..., None] + len(self.toker) - 18], dim=-1)

        assert 'max_length' in kwargs
        kwargs['max_length'] = kwargs['max_length'] + decoder_input_ids.size(1)
        kwargs['use_cache'] = True

        if len(self.toker) > self.toker.vocab_size:
            bad_words_ids = [[i] for i in range(self.toker.vocab_size, len(self.toker))]
            kwargs['bad_words_ids'] = bad_words_ids

        generations = super().generate(
            attention_mask=attention_mask,
            encoder_outputs=encoder_outputs,
            decoder_input_ids=decoder_input_ids,
            **kwargs
        )
        return encoded_info, generations[:, decoder_input_ids.size(1):]
