#include <windows.h>
#include <commctrl.h>
#include <stdio.h>
#include "resource.h"

HINSTANCE hInst;

void ONGraficar(HWND hwnd) {
    HDC hdc = GetDC(hwnd);

    // Fondo blanco
    HBRUSH bgBrush = CreateSolidBrush(RGB(255, 255, 255));
    RECT clientRect;
    GetClientRect(hwnd, &clientRect);
    FillRect(hdc, &clientRect, bgBrush);
    DeleteObject(bgBrush);

    // Coordenadas para el sistema de ejes
    int centerX = (clientRect.right - clientRect.left) / 2;
    int centerY = (clientRect.bottom - clientRect.top) / 2;

    // Dibujar cuadrícula
    HPEN gridPen = CreatePen(PS_SOLID, 1, RGB(220, 220, 220));
    SelectObject(hdc, gridPen);
    for (int x = centerX % 20; x < clientRect.right; x += 20)
        MoveToEx(hdc, x, 0, NULL), LineTo(hdc, x, clientRect.bottom);
    for (int y = centerY % 20; y < clientRect.bottom; y += 20)
        MoveToEx(hdc, 0, y, NULL), LineTo(hdc, clientRect.right, y);
    DeleteObject(gridPen);

    // Dibujar ejes X y Y
    HPEN axisPen = CreatePen(PS_SOLID, 2, RGB(0, 0, 0));
    SelectObject(hdc, axisPen);
    MoveToEx(hdc, centerX, 0, NULL); LineTo(hdc, centerX, clientRect.bottom);
    MoveToEx(hdc, 0, centerY, NULL); LineTo(hdc, clientRect.right, centerY);
    DeleteObject(axisPen);

    // Punto lleno (abajo izquierda)
    HBRUSH redBrush = CreateSolidBrush(RGB(150, 0, 0));
    SelectObject(hdc, redBrush);
    Ellipse(hdc, centerX - 100 - 5, centerY + 100 - 5, centerX - 100 + 5, centerY + 100 + 5);
    DeleteObject(redBrush);

    // Punto hueco (en el eje Y arriba)
    HPEN redPen = CreatePen(PS_SOLID, 2, RGB(150, 0, 0));
    SelectObject(hdc, redPen);
    SelectObject(hdc, GetStockObject(HOLLOW_BRUSH));
    Ellipse(hdc, centerX - 5, centerY - 100 - 5, centerX + 5, centerY - 100 + 5);
    DeleteObject(redPen);

    ReleaseDC(hwnd, hdc);
}


BOOL CALLBACK DlgMain(HWND hwndDlg, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    switch(uMsg)
    {
    case WM_INITDIALOG:
    {
    }
    return TRUE;

    case WM_CLOSE:
    {
        EndDialog(hwndDlg, 0);
    }
    return TRUE;

    case WM_COMMAND:
    {
        switch(LOWORD(wParam))
        {
            case BTN_GRAF:{
                ONGraficar(hwndDlg);
                return TRUE;
        }
            case IDCANCEL:
                EndDialog(hwndDlg,0);
                return TRUE;
            }
            break;
    }
    return TRUE;
    }
    return FALSE;
}


int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd)
{
    hInst=hInstance;
    InitCommonControls();
    return DialogBox(hInst, MAKEINTRESOURCE(DLG_MAIN), NULL, (DLGPROC)DlgMain);
}