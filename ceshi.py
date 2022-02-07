# include "mainwindow.h"
# include <QApplication>

# include <opencv2/core/core.hpp>
# include <opencv2/highgui/highgui.hpp>
# include <opencv2/imgproc/imgproc.hpp>

using
namespace
cv;

int
main(int
argc, char * argv[])
{
    QApplication
a(argc, argv);

cv::Mat
image = imread("D:\python\yolo\test_images\IMG_20210506_103652 (2).jpg");
namedWindow("Display window", WINDOW_AUTOSIZE);
imshow("Display window", image);
waitKey(0);

MainWindow
w;
w.show();
return a.exec();
}
