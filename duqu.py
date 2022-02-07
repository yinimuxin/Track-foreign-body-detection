# include "mainwindow.h"
# include <QApplication>

# include <opencv4/core/core.hpp>
# include <opencv4/highgui/highgui.hpp>
# include <opencv4/imgproc/imgproc.hpp>

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
image = imread("‪D:\python\yolo\jiancejieguo\IMG_20210506_103851.jpg");
namedWindow("Display window", WINDOW_AUTOSIZE);
imshow("Display window", image);
waitKey(0);

MainWindow
w;
w.show();
return a.exec();
}
