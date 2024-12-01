import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.*;
import javax.imageio.ImageIO;
import javax.sound.sampled.*;
import javax.swing.Timer;

public class SlidingPuzzleGame {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new GameFrame());
    }
}

class GameFrame extends JFrame {
    private GamePanel gamePanel;

    public GameFrame() {
        setTitle("Sliding Puzzle Game");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        gamePanel = new GamePanel(this);
        add(gamePanel, BorderLayout.CENTER);

        pack();
        setLocationRelativeTo(null);
        setVisible(true);
    }
}

abstract class PuzzlePanel extends JPanel {
    protected JButton[][] buttons;
    protected int emptyRow, emptyCol;
    protected int moves;
    protected String playerName;
    protected BufferedImage fullImage;

    public abstract void initializeGame(BufferedImage image, int gridSize);

    public boolean moveTile(int targetRow, int targetCol) {
        if (isValidMove(targetRow, targetCol)) {
            JButton[][] buttons = getButtons();
            Icon tempIcon = buttons[targetRow][targetCol].getIcon();
            String tempText = buttons[targetRow][targetCol].getText();
            buttons[emptyRow][emptyCol].setIcon(tempIcon);
            buttons[emptyRow][emptyCol].setText(tempText);
            buttons[targetRow][targetCol].setIcon(null);
            buttons[targetRow][targetCol].setText("");
            emptyRow = targetRow;
            emptyCol = targetCol;
            moves++;
            return true;
        }
        return false;
    }

    protected boolean isValidMove(int targetRow, int targetCol) {
        return (Math.abs(targetRow - emptyRow) == 1 && targetCol == emptyCol) ||
                (Math.abs(targetCol - emptyCol) == 1 && targetRow == emptyRow);
    }

    protected abstract JButton[][] getButtons();

    public abstract boolean checkWinCondition();
}
