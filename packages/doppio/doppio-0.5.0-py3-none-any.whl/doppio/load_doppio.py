import types    # 동적 모듈 생성과 관련된 모듈로 파이썬 2버전에서는 imp 모듈을 사용함
import marshal    # 코드 로딩과 관련된 모듈
import pkg_resources
import os



def doppio(dataset, split_dir, task_info, augmentation = None):

   
    resource_package = pkg_resources.get_distribution('doppio').location
    config_path = os.path.join(resource_package,'doppio/test.txt')

    pyc = open(config_path, 'rb').read()    # 바이트 코드를 읽어옴
    code = marshal.loads(pyc[16:])    # pyc에서 헤더를 제외한 코드를 로딩함

    #print(code)
    module = types.ModuleType('hello')    # 'hello'라는 새로운 모듈 생성, 파이썬2에서는 imp.new_module() 함수를 사용할 수 있음

    exec(code, module.__dict__)    # pyc 코드와 모듈을 연결함


    dataloader = module.doppio(dataset=dataset, split_dir=split_dir, task_info=task_info, augmentation=augmentation)    # hello 모듈의 printHello() 함수 호출

    return dataloader
