from model import *

if __name__ == "__main__":
    Base.metadata.create_all(bind = engine)
