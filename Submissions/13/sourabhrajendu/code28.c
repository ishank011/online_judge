#include <stdio.h>
#include <GL/glut.h>
#include <math.h>

#define PI 3.14159265358979323846

float X1,Y1,X2,Y2;
float P1,Q1,P2,Q2;

int n;

struct point
{
	float x;
	float y;
};

struct point org_point[128];
struct point new_point[128];

void mul3_3(float* a, float* b, float* c)
{
	float p[3][3],q[3][3],r[3][3];

	int i,j,k;

	for(i=0;i<3;i++)
	{
		for(j=0;j<3;j++)
		{
			p[i][j] = *(a+i*3+j);
		}
	}

	for(i=0;i<3;i++)
	{
		for(j=0;j<3;j++)
		{
			q[i][j] = *(b+i*3+j);
		}
	}

	for(i=0;i<3;i++)
	{
		for(j=0;j<3;j++)
		{
			r[i][j] = 0.00f;

			for(k=0;k<3;k++)
			{
				r[i][j] += p[i][k]*q[k][j];
			}
		}
	}

	for(i=0;i<3;i++)
	{
		for(j=0;j<3;j++)
		{
			*(c+i*3+j) = r[i][j];
		}
	}
}

void mul3_1(float* a, float* b, float* c)
{
	float p[3][3],q[3][1],r[3][1];

	int i,j,k;

	for(i=0;i<3;i++)
	{
		for(j=0;j<3;j++)
		{
			p[i][j] = *(a+i*3+j);
		}
	}

	for(i=0;i<3;i++)
	{
		for(j=0;j<1;j++)
		{
			q[i][j] = *(b+i*1+j);
		}
	}

	for(i=0;i<3;i++)
	{
		for(j=0;j<1;j++)
		{
			r[i][j] = 0.00f;

			for(k=0;k<3;k++)
			{
				r[i][j] += p[i][k]*q[k][j];
			}
		}
	}

	for(i=0;i<3;i++)
	{
		for(j=0;j<1;j++)
		{
			*(c+i*1+j) = r[i][j];
		}
	}
}

void copy(float* a, float* b)
{
	int i;

	for(i=0;i<9;i++)
	{
		a[i] = b[i];
	}
}

void func()
{
	/* Clears buffers to preset values */
	glClear(GL_COLOR_BUFFER_BIT);

	/* Plot the points */
	glBegin(GL_LINES);

	glColor3f(0.0,0.0,0.0);

	glVertex3f(-940.00, 0.00, 0.00);
	glVertex3f(-50.00, 0.00, 0.00);

	glVertex2f(-940.00, 0.00);
	glVertex2f(-940.00, 540.00);

	glVertex2f(0.00, 0.00);
	glVertex2f(960.00, 0.00);

	glVertex2f(0.00, 0.00);
	glVertex2f(0.00, 540.00);

	glEnd();

	glBegin(GL_LINE_STRIP);

	glVertex2f(X1 - 940.00f, Y1);
	glVertex2f(X1 - 940.00f, Y2);
	glVertex2f(X2 - 940.00f, Y2);
	glVertex2f(X2 - 940.00f, Y1);
	glVertex2f(X1 - 940.00f, Y1);

	glEnd();

	glBegin(GL_LINE_STRIP);

	glVertex2f(P1, Q1);
	glVertex2f(P1, Q2);
	glVertex2f(P2, Q2);
	glVertex2f(P2, Q1);
	glVertex2f(P1, Q1);

	glEnd();

	int i;

	glBegin(GL_POLYGON);

	glColor3f(0.0, 1.0, 0.0);

	for(i=0;i<n;i++)
	{
		glVertex2f(org_point[i].x - 940.00f, org_point[i].y);
	}

	glEnd();

	glBegin(GL_POLYGON);

	glColor3f(0.0, 0.0, 1.0);

	for(i=0;i<n;i++)
	{
		glVertex2f(new_point[i].x, new_point[i].y);
	}

	glEnd();

	glFlush();
}

void printMat(float* a)
{
	int i,j;
	for(i=0;i<3;i++)
	{
		for(j=0;j<3;j++)
		{
			printf("%f\t",*(a+i*3+j));
		}
		printf("\n");
	}
}

void Init()
{
  /* Set clear color to white */
  glClearColor(1.0,1.0,1.0,0);
  /* Set fill color to black */
  glColor3f(0.0,0.0,0.0);
  /* glViewport(0 , 0 , 640 , 480); */
  /* glMatrixMode(GL_PROJECTION); */
  /* glLoadIdentity(); */
  gluOrtho2D(-960 , 960 , -540 , 540);
}

int main(int argc, char*argv[])
{

	setbuf(stdout,NULL);

	float mat[3][3];
	float temp[3][3];
	float temp_mat[3][3];

	int i,j;
	for(i=0;i<3;i++)
	{
		for(j=0;j<3;j++)
		{
			if(i == j)
				mat[i][j] = 1.00f;
			else
				mat[i][j] = 0.00f;
		}
	}

	printf("Enter lower left co-ordinates of window (0 < x < 940 , 0 < y < 540)\n");
	scanf("%f %f", &X1, &Y1);

	printf("Enter upper right co-ordinates of window (0 < x < 940 , 0 < y < 540)\n");
	scanf("%f %f", &X2, &Y2);

	if(X2 <= X1 || Y2 <= Y1 || X1 <= 0 || X1 >= 940 || Y1 <= 0 || Y1 >= 540 || X2 <= 0 || X2 >= 940 || Y2 <= 0 || Y2 >= 540)
	{
		printf("Invalid window coordinates\n");
		return 0;
	}

	printf("Enter the number of points\n");
	scanf("%d", &n);

	for(i=0;i<n;i++)
	{
		scanf("%f %f", &org_point[i].x, &org_point[i].y);

		if(org_point[i].x > X2 || org_point[i].x < X1)
		{
			printf("Invalid X coordinate for point\n");
			return 0;
		}

		if(org_point[i].y > Y2 || org_point[i].y < Y1)
		{
			printf("Invalid Y coordinate for point\n");
			return 0;
		}

	}

	printf("Enter lower left co-ordinates of viewport (0 < x < 940 , 0 < y < 540)\n");
	scanf("%f %f", &P1, &Q1);

	printf("Enter upper right co-ordinates of viewport (0 < x < 940 , 0 < y < 540)\n");
	scanf("%f %f", &P2, &Q2);

	if(P2 <= P1 || Q2 <= Q1 || P1 <= 0 || P1 >= 940 || Q1 <= 0 || Q1 >= 540 || P2 <= 0 || P2 >= 940 || Q2 <= 0 || Q2 >= 540)
	{
		printf("Invalid viewport coordinates\n");
		return 0;
	}

	float tx = -1.00f * X1;
	float ty = -1.00f * Y1;

	float sx = (P2-P1)/(X2-X1);
	float sy = (Q2-Q1)/(Y2-Y1);

	printMat(&mat[0][0]);

	temp[0][0] = 1.00f, temp[0][1] = 0.00f, temp[0][2] = tx;
	temp[1][0] = 0.00f, temp[1][1] = 1.00f, temp[1][2] = ty;
	temp[2][0] = 0.00f, temp[2][1] = 0.00f, temp[2][2] = 1.00f;

	mul3_3(&temp[0][0], &mat[0][0], &temp_mat[0][0]);

	copy(&mat[0][0], &temp_mat[0][0]);
	printMat(&mat[0][0]);

	temp[0][0] = sx, temp[0][1] = 0.00f, temp[0][2] = 0.00f;
	temp[1][0] = 0.00f, temp[1][1] = sy, temp[1][2] = 0.00f;
	temp[2][0] = 0.00f, temp[2][1] = 0.00f, temp[2][2] = 1.00f;

	mul3_3(&temp[0][0], &mat[0][0], &temp_mat[0][0]);

	copy(&mat[0][0], &temp_mat[0][0]);

	printMat(&mat[0][0]);

	tx = P1;
	ty = Q1;

	temp[0][0] = 1.00f, temp[0][1] = 0.00f, temp[0][2] = tx;
	temp[1][0] = 0.00f, temp[1][1] = 1.00f, temp[1][2] = ty;
	temp[2][0] = 0.00f, temp[2][1] = 0.00f, temp[2][2] = 1.00f;

	mul3_3(&temp[0][0], &mat[0][0], &temp_mat[0][0]);

	copy(&mat[0][0], &temp_mat[0][0]);
	printMat(&mat[0][0]);


	float temp_1[3][1];
	float temp_2[3][1];

	for(i=0;i<n;i++)
	{
		temp_1[0][0] = org_point[i].x, temp_1[1][0] = org_point[i].y, temp_1[2][0] = 1.00f;

		mul3_1(&mat[0][0], &temp_1[0][0], &temp_2[0][0]);
		new_point[i].x = temp_2[0][0];
		new_point[i].y = temp_2[1][0];
	}

	/* Initialise GLUT library */
	glutInit(&argc,argv);
	/* Set the initial display mode */
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
	/* Set the initial window position and size */
	glutInitWindowPosition(0,0);
	glutInitWindowSize(1920,1080);
	/* Create the window with title "DDA_Line" */
	glutCreateWindow("Window to Viewport");
	/* Initialize drawing colors */
	Init();
	/* Call the displaying function */
	glutDisplayFunc(func);
	/* Keep displaying until the program is closed */
	glutMainLoop();

}
