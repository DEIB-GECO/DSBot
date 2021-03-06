"""
Assumes that the context contains the dataset and the pipeline to use and update, and the old result.
{
    'pipeline': pipeline,
    'result': base64oldResult,
    'start_work': callback to start the pipeline execution
}
"""
import logging

from mmcc_framework import Response

import ir.ir_exceptions
from tuning.problem_helper import solve_problem, MissingSolutionError
from tuning.tuning_mixins import update_pipeline, TuningParMixin, TuningOpOptionsMixin


def start(_, kb, context, __):
    """Returns the result and a welcome utterance."""
    payload = {
        'status': 'choose_problem',
        'result': context['result'],
    }
    return Response(kb, context, True, payload=payload)


def choose_problem(data, kb, context, _):
    """In this step the user can try to explain the problem he is facing.

    If data['intent'] is 'skip' the process to continues without selecting a problem.
    Otherwise data['intent'] can be a problem keyword.
    """
    try:
        intent = data['intent']
        if intent == 'skip':
            context['solution'] = None
            payload = {
                'status': 'edit_param',
                'pipeline': [e.to_json() for e in context['pipeline']],
            }
            return Response(kb, context, True, utterance=kb['no_highlights_sentence'], payload=payload)

        utterance = _query_impl(intent, kb, context)
        payload = {
            'status': 'edit_param',
            'pipeline': [e.to_json() for e in context['pipeline']],
        }
        return Response(kb, context, True, utterance=utterance, payload=payload)

    except KeyError:
        msg = f'Received data without intent: {str(data)}'
        logging.getLogger(__name__).error(msg)
    except MissingSolutionError as err:
        logging.getLogger(__name__).warning(err)
        msg = kb['problem_err']
    return Response(kb, context, False, utterance=msg)


def _query_impl(intent, kb, context) -> str:
    solution = solve_problem(intent, context['pipeline'])
    context['solution'] = solution
    context['pipeline'] = update_pipeline(context['pipeline'], solution.relevant_params)
    utterance = solution.sentence + ' ' + kb['edit_param_sentence']
    return utterance


def edit_param(data, kb, context, _):
    """In this step the user can edit the pipeline.

    data['intent'] can be 'set', 'reset', 'set_module', or 'run', the latter causes the pipeline to be run.
    data['module'] contains the module of the parameter to change or the module to change.
    data['parameter'] contains the parameter name to change.
    data['value'] contains the new value.
    """
    intent = data.get('intent', None)
    if intent is None:
        msg = f'Received data with missing intent or entities: {str(data)}'
        logging.getLogger(__name__).error(msg)

    elif intent == 'run':
        context['start_work'](context['pipeline'])
        return Response(kb, context, True, payload={'status': 'end'})

    elif intent == 'set' and 'module' in data and 'parameter' in data and 'value' in data:
        msg = _set_impl(data, kb, context)

    elif intent == 'reset' and 'module' in data and 'parameter' in data:
        msg = _reset_impl(data, kb, context)

    elif intent == 'set_module' and 'module' in data and 'value' in data:
        msg = _set_module_impl(data, kb, context)

    else:
        try:
            msg = _query_impl(intent, kb, context)
        except MissingSolutionError as err:
            logging.getLogger(__name__).warning(err)
            msg = kb['problem_err_edit']

    payload = {'status': 'edit_param', 'pipeline': [e.to_json() for e in context['pipeline']]}
    return Response(kb, context, False, payload=payload, utterance=msg)


def _set_impl(data, kb, context) -> str:
    param, module = TuningParMixin.reverse_pretty(data['parameter'], context['pipeline'], data['module'])
    if param is None:
        msg = kb['no_param_err'] + data['parameter']
    else:
        try:
            module.get_param(param.name).tune_value(data['value'])
            msg = kb['values_updated']
        except ir.ir_exceptions.IncorrectValue:
            msg = kb['value_err']
    return msg


def _set_module_impl(data, kb, context) -> str:
    module, parent = TuningOpOptionsMixin.reverse_pretty(data['value'], context['pipeline'], data['module'])
    if module is None:
        msg = kb['no_module_err'] + data['module']
    else:
        parent.set_model(module.name)
        msg = kb['values_updated']
    return msg


def _reset_impl(data, kb, context) -> str:
    param, module = TuningParMixin.reverse_pretty(data['parameter'], context['pipeline'], data['module'])
    if param is None:
        msg = kb['no_param_err'] + data['parameter']
    else:
        del module.get_param(param.name).value
        msg = kb['values_updated']
    return msg


my_callbacks = {
    "start": start,
    "choose_problem": choose_problem,
    "edit_param": edit_param,
}
