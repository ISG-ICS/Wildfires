import argparse
import torch
import rootpath

rootpath.append()
import yutong_nlp.textcnn_mine.mydatasets_embed as mydatasets_embed
import yutong_nlp.textcnn_mine.train as train
from yutong_nlp.textcnn_mine.CNN_text1 import CNN_Text


def handle_args():
    parser = argparse.ArgumentParser(description='CNN twitter classifier')
    # learning
    parser.add_argument('-lr', type=float, default=0.001, help='initial learning rate [default: 0.001]')
    # parser.add_argument('-weight-decay', type=float, default=0.0001, help='weight decay, L2 penalty [default: 0.0001]')
    parser.add_argument('-epochs', type=int, default=4, help='number of epochs for train [default: 256]')
    parser.add_argument('-batch-size', type=int, default=64, help='batch size for training [default: 64]')
    parser.add_argument('-log-interval', type=int, default=1,
                        help='how many steps to wait before logging training status [default: 1]')
    parser.add_argument('-test-interval', type=int, default=100,
                        help='how many steps to wait before testing [default: 100]')
    parser.add_argument('-save-interval', type=int, default=500,
                        help='how many steps to wait before saving [default: 500]')
    parser.add_argument('-save-dir', type=str, default='snapshot', help='where to save the snapshot')
    parser.add_argument('-early-stop', type=int, default=1000,
                        help='iteration numbers to stop without performance increasing')
    parser.add_argument('-save-best', type=bool, default=True, help='whether to save when get best performance')
    # parser.add_argument('-shuffle', action='store_true', default=False, help='shuffle the data every epoch')
    parser.add_argument('-stride', type=int, default=1, help='stride for conv2d')
    parser.add_argument('-glove-embed', type=bool, default=True, help='whether to use the glove twitter embedding or not')
    parser.add_argument('-glove-embed-train', type=bool, default=True, help='whether to train the glove embedding or not')
    parser.add_argument('-multichannel', type=bool, default=True, help='multiple channel of input')

    # model
    parser.add_argument('-dropout', type=float, default=0.7, help='the probability for dropout [default: 0.5]')
    parser.add_argument('-max-norm', type=float, default=3.0, help='l2 constraint of parameters [default: 3.0]')
    parser.add_argument('-embed-dim', type=int, default=100, help='number of embedding dimension [default: 128]')
    parser.add_argument('-kernel-num', type=int, default=100, help='number of each kind of kernel')
    parser.add_argument('-kernel-sizes', type=str, default='2,2,2',
                        help='comma-separated kernel size to use for convolution')
    parser.add_argument('-static', action='store_true', default=False, help='fix the embedding')

    # device
    parser.add_argument('-device', type=int, default=-1,
                        help='device to use for iterate data, -1 mean cpu [default: -1]')
    parser.add_argument('-no-cuda', action='store_true', default=False, help='disable the gpu')

    # option
    parser.add_argument('-snapshot', type=str, default=None, help='filename of model snapshot [default: None]')
    parser.add_argument('-predict', type=str, default=None, help='predict the sentence given')
    parser.add_argument('-test', action='store_true', default=False, help='train or test')

    # workflow
    parser.add_argument('-read-path', type=str, default='./dataset/',
                        help='the path to the labeled data')
    parser.add_argument('-pos-num', type=int, default=1000, help='the number of positive tweets [default: 5000]')
    parser.add_argument('-neg-num', type=int, default=1000, help='the number of negative tweets [default: 5000]')
    parser.add_argument('-workflow', type=str, default='w2', help='which workflow to analysis [default: w2]')
    parser.add_argument('-keywords', type=str, default='cc', help='the keywords of the workflow [default: cc]')
    parser.add_argument('-pad-len', type=int, default=64, help='the length of padding [default: 64]')
    parser.add_argument('-worker-num', type=int, default=2, help='the number of workers')
    parser.add_argument('-pos-weight', type=float, default=1.0, help='the pos class penalty')

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = handle_args()
    args.cuda = (not args.no_cuda) and torch.cuda.is_available(); del args.no_cuda

    print("\nParameters:")
    for attr, value in sorted(args.__dict__.items()):
        print("\t{}={}".format(attr.upper(), value))

    dataset = mydatasets_embed.My_datasets(args)
    train_loader, validate_loader, test_loader, vocab_len, weights = dataset.get_train_validate_test_loader()

    # set the random seed
    torch.manual_seed(3)
    torch.cuda.manual_seed_all(3)

    model = CNN_Text(args, vocab_len, weights)

    my_loss = train.My_loss()

    weight = torch.Tensor([args.pos_num / 1000, args.neg_num / 1000 * args.pos_weight])  #.cuda()

    train.train(train_loader, validate_loader, test_loader, model, my_loss, weight, args)
