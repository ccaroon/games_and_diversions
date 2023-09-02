class Mandelbrot {
private:
    int xMin;
    int xMax;
    int yMin;
    int yMax;
    static const int width  = 96;
    static const int height = 64;
    int buffer[height][width];

public:
    Mandelbrot(int,int,int,int);
    void compute(int);
    void display(void);
    void display2(void);
    int* getRow(int);
};
