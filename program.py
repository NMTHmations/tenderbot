from modules import TrainModel
from modules import SwipeAutomator
from modules import CollectProfilePhotos
import sys
import argparse
import traceback

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tenderbot - Automated Tinder tool")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    swipe = subparsers.add_parser('AutoSwipe', help='Swipe automatically right or sorts out the profiles with CNN AI model')
    swipe.add_argument('-f','--file',type=str,required=False,help="The keras model's path")
    swipe.add_argument('-s','--start',type=int,required=False,help="Set starting hours (default 6pm)")
    swipe.add_argument('-e','--end',type=int,required=False,help="Set ending hours (default 10pm)")
    swipe.add_argument('-p','--phone',type=int,required=True,help="Phone number")
    swipe.add_argument('--noCNN',required=False,help="Disable CNN model. The tool swipes always right",action='store_false')
    
    model = subparsers.add_parser('TrainModel',help="Train convolutional neural network (CNN) model based on dataset")
    model.add_argument('--file',type=str,required=True,help="The file path for newly created model")
    model.add_argument('--train',type=str,required=True,help="Train dataset path")
    model.add_argument('--test',type=str,required=True,help="Test dataset path")
    model.add_argument('--epoch','-e',type=int,required=False,help="Set epochs (default 10)")
    model.add_argument('--batch','-b',type=int,required=False,help="Set batch size (default 10)")
    model.add_argument('--targetHeight','-tH',type=int,required=False,help="Set target height (default 224)")
    model.add_argument('--targetWidth','-tW',type=int,required=False,help="Set target width (default 224)")
    
    collectPhotos = subparsers.add_parser('collectPhotos',help="Collect photos for learning")
    collectPhotos.add_argument('-p','--phone',type=int,required=True,help="Phone number")
    collectPhotos.add_argument('-cT','--cropTop',type=str,required=True,help="Top cropping position")
    collectPhotos.add_argument('-cB','--cropBottom',type=str,required=True,help="Bottom cropping position")
    
    args = parser.parse_args()
    
    try:
        if args.command == 'SwipeAutomator':
            swiper = SwipeAutomator.SwipeAutomator(args.phone,
                                          args.file,
                                          args.start if args.start != None else 18,
                                          args.end if args.end != None else 22)
            swiper.SwipeCNN(args.noCNN)
        elif args.command == "TrainModel":
            model = TrainModel.TrainModel(args.train,args.test,
                                          args.batch if args.batch != None else 10,
                                          args.epochs if args.epochs != None else 10,
                                          args.targetWidth if args.targetWidth != None else 224,
                                          args.targetHeight if args.targetHeight != None else 224,
                                          args.file)
            model.GenerateModel()
        elif args.command == "collectPhotos":
            if len(args.cropTop.split(',')) == 2 and len(args.cropBottom.split(',')) == 2:
                cropTop = (int(args.cropTop.split(',')[0]),int(args.cropTop.split(',')[1]))
                cropBottom = (int(args.cropBottom.split(',')[0]),int(args.cropBottom.split(',')[1]))
                profiles = CollectProfilePhotos.CollectProfilePhotos(args.phone,cropTop,cropBottom)
                profiles.yieldPhotos()
            else:
                raise Exception("Invalid cropTop or cropBottom format")
    except Exception as e:
        traceback.print_exc()
        exit(1)