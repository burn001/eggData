import pickle, os

def add_to_pickle(filename, itm):
    """(범용)피클 파일을 열어서 새로운 데이터를 추가하는 함수
    arguments:
    filename -- 저장하고자 하는 피클 파일명(존재하지 않을 시 새로 만들게 됨)
    itm -- 피클로 저장하려는 객체
    """
    with open(filename,'a+b') as f:
        pickle.dump(itm, f, pickle.HIGHEST_PROTOCOL)
    return

def dump_to_pickle(filename, itm):
    """(범용)피클 파일에 itm을 통째로 저장
    arguments:
    filename -- 저장하고자 하는 피클 파일명(존재하지 않을 시 새로 만들게 됨)
    itm -- 피클로 저장하려는 객체
    """
    with open(filename,'wb') as f:
        pickle.dump(itm, f, pickle.HIGHEST_PROTOCOL)
    return

def load_dumped_pickle(filename):
    """(범용)피클이 한꺼번에 dump된 경우에 사용, 피클 데이터 한 개를 로드하여 반환
    """
    with open(filename,'rb') as f:
        return pickle.load(f)

def pickle_loader(f):
    """(범용)피클 데이터를 하나씩 반환하는 iterator
    arguments:
    f -- 피클 파일 객체, 파일명이 아님! with open() as f: 이후에 pickle_loader를 사용하는 것을 상정하고 작성함
    """
    try:
        while True:
            yield pickle.load(f)
    except EOFError:
        pass

class pickle_iterator():
    """(범용)피클 파일을 한 줄 씩 반환하는 iterator
    """
    def __init__(self, filename):
        self.filename=filename
        self.len=0
    def __iter__(self):
        if os.path.isfile(self.filename):
            with open(self.filename,'rb') as f:
                try:
                    while True:
                        yield pickle.load(f)
                except EOFError:
                    pass
        else:
            print("No file.")
    def __len__(self):
        if self.len==0:
            if os.path.isfile(self.filename):
                with open(self.filename,'rb') as f:
                    try:
                        while True:
                            pickle.load(f)
                            self.len+=1
                    except EOFError:
                        pass
                return self.len
            else:
                return 0
        else:
            return self.len
        
def load_dataset(filename):
    """(범용)피클로 저장된 데이터셋을 list로 가져오는 함수
    arguments:
    filename -- 피클 파일 이름(확장자 포함)
    """
    dataset=[]
    if os.path.isfile(filename):
        with open(filename,'rb') as f:
            for x in pickle_loader(f):
                dataset.append(x)
    else:
        print('No file.')
    return dataset

def save_dataset(filename, dataset):
    """
    """
    with open(filename,'wb') as f:
        for x in dataset:
            pickle.dump(x, f, pickle.HIGHEST_PROTOCOL)
            
def get_len(filename):
    """(범용) pickle로 저장된 데이터의 길이를 구하는 함수
    arguments:
    filename -- 저장된 피클 파일 이름(확장자 포함)
    """
    ret=0
    
    if os.path.isfile(filename):
        for x in pickle_iterator(filename):
            ret+=1
        return ret
    else:
        return 0