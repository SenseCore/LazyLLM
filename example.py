import lazyllm
try:
   from builtins import package, dataproc, finetune, deploy, launchers, validate
except ImportError:
   from lazyllm import package, dataproc, finetune, deploy, launchers, validate

@lazyllm.llmregister('dataproc')
def gen_data(idx):
    print(f'idx {idx}: gen data done')
    return package(idx + 1, idx + 1)

@lazyllm.llmregister('Validate')
def eval_stage1(url, port):
    print(f'url {url}:{port} eval_stage1 done')

@lazyllm.llmregister('Validate')
def eval_stage2(url, port):
    print(f'url {url}:{port} eval_stage2 done')

@lazyllm.llmregister('validate')
def eval_all(url1, url2):
    print(f'eval all: {url1} and {url2}  eval_all done')

ppl = lazyllm.pipeline(
    dataproc.gen_data(),
    lazyllm.parallel(
        lazyllm.pipeline(
            finetune.alpacalora(base_model='./base-model1', target_path='./finetune-target1', launcher=launchers.slurm()),
            deploy.lightllm('http://www.myserver1.com'),
            post_action=validate.eval_stage1,
        ),
        lazyllm.pipeline(
            finetune.alpacalora(base_model='./base-model2', target_path='./finetune-target2', launcher=launchers.slurm),
            deploy.lightllm('http://www.myserver2.com', 8080),
            post_action=validate.eval_stage1,
        ),
    ),
    validate.eval_all,
)
ppl.run(0)