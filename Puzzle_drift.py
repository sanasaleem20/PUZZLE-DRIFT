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

Class Player1Panel extends PuzzlePanel {

    GamePanel gamePanel;



    Public Player1Panel(String name, GamePanel gamePanel) {

        playerName = name;

        this.gamePanel = gamePanel;

        setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.BLUE, 3), playerName));

    }



    @Override

    Public void initializeGame(BufferedImage image, int gridSize) {

        removeAll();

        setLayout(new GridLayout(gridSize, gridSize, 0, 0));

        buttons = new JButton[gridSize][gridSize];

        fullImage = image;



        ArrayList<Integer> tiles = new ArrayList<>();

        For (int i = 0; i < gridSize * gridSize; i++) {

            Tiles.add(i);

        }

        Collections.shuffle(tiles);



        Int panelSize = 778;

        setPreferredSize(new Dimension(panelSize, panelSize));

        int buttonSize = panelSize / gridSize;



        for (int i = 0; i < gridSize; i++) {

            for (int j = 0; j < gridSize; j++) {

                int tile = tiles.get(i * gridSize + j);

                buttons[i][j] = new JButton();

                buttons[i][j].setPreferredSize(new Dimension(buttonSize, buttonSize));

                buttons[i][j].setMargin(new Insets(0, 0, 0, 0));

                buttons[i][j].setBorder(BorderFactory.createLineBorder(Color.BLACK));

                if (tile == gridSize * gridSize – 1) {

                    buttons[i][j].setText(“”);

                    emptyRow = i;

                    emptyCol = j;

                } else {

                    BufferedImage tileImage = image.getSubimage(

                            (tile % gridSize) * (image.getWidth() / gridSize),

                            (tile / gridSize) * (image.getHeight() / gridSize),

                            Image.getWidth() / gridSize,

                            Image.getHeight() / gridSize

                    );

                    Image scaledImage = tileImage.getScaledInstance(buttonSize, buttonSize, Image.SCALE_SMOOTH);

                    Buttons[i][j].setIcon(new ImageIcon(scaledImage));

                    Buttons[i][j].setText(String.valueOf(tile + 1));

                    Buttons[i][j].setHorizontalTextPosition(JButton.CENTER);

                    Buttons[i][j].setVerticalTextPosition(JButton.CENTER);

                    Buttons[i][j].setForeground(new Color(0, 0, 0, 0));

                }

                Final int finalI = i;

                Final int finalJ = j;

                Buttons[i][j].addActionListener(e -> {

                    If (moveTile(finalI, finalJ)) {

                        gamePanel.playMoveSound();

                        gamePanel.updateMovesLabels();

                        gamePanel.checkWinCondition();

                    }

                });

                Add(buttons[i][j]);

            }

        }

        Revalidate();

        Repaint();

    }



    @Override

    Protected JButton[][] getButtons() {

        Return buttons;

    }



    @Override

    Public boolean checkWinCondition() {

        Int gridSize = buttons.length;

        For (int i = 0; i < gridSize; i++) {

            For (int j = 0; j < gridSize; j++) {

                Int expectedTile = i * gridSize + j;

                If (expectedTile < gridSize * gridSize – 1) {

                    If (!buttons[i][j].getText().equals(String.valueOf(expectedTile + 1))) {

                        Return false;

                    }

                }

            }

        }

        Return true;

    }



    @Override

    Protected void paintComponent(Graphics g) {

        Super.paintComponent(g);

        If (!gamePanel.isTwoPlayerMode) {

            Try {

                BufferedImage backgroundImage = ImageIO.read(new File(“C:\\Users\\Nuzhat\\Downloads\\b2.jpg”));

                g.drawImage(backgroundImage, 0, 0, getWidth(), getHeight(), this);

            } catch (IOException e) {

                e.printStackTrace();

            }

        }

    }

}

Class Player2Panel extends Player1Panel {

    Public Player2Panel(String name, GamePanel gamePanel) {

        Super(name, gamePanel);

        setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.RED, 3), playerName));

    }

}

Class GamePanel extends JPanel {

    Private GameFrame frame;

    Private PuzzlePanel player1Panel, player2Panel;

    Private JComboBox<String> categorySelect;

    Private JLabel timerLabel, player1MovesLabel, player2MovesLabel;

    Private Timer gameTimer;

    Private int timeElapsed;

    Private int gridSize;

    Boolean isTwoPlayerMode = false;

    Private boolean showNumbers = false;

    Private BufferedImage image;

    Private Clip backgroundMusic;

    Private boolean isMusicPlaying = false;

    Private Clip moveSoundClip;

    Private boolean isSoundEnabled = true;

    Private JSlider volumeSlider;

    Private Clip victoryMusic;

    Private boolean isVictoryMusicPlaying = false;



    Private JButton showImageButton;

    Private JButton showNumbersButton;

    Private JButton puzzleSwapButton;

    Private int showImageCount = 2;

    Private int showNumbersCount = 2;

    Private int puzzleSwapCount = 2;

    Private Timer showImageTimer;

    Private Timer showNumbersTimer;

    Private Timer puzzleSwapTimer;



    Private JButton homeButton;

    Private JButton soundButton;



    Private static final String[] categories = {“Cartoons”, “Sports”, “Anime”, “Merged Objects”, “Animals”};

    Private static final String[][] imagePaths = {

            {“C:\\Users\\Nuzhat\\Downloads\\9.jpg”, “C:\\Users\\Nuzhat\\Downloads\\8.jpg”, “C:\\Users\\Nuzhat\\Downloads\\7.jpg”},

            {“C:\\Users\\Nuzhat\\Downloads\\14.jpg”, “C:\\Users\\Nuzhat\\Downloads\\15.jpg”, “C:\\Users\\Nuzhat\\Downloads\\16.jpg”},

            {“C:\\Users\\Nuzhat\\Downloads\\1.jpg”, “C:\\Users\\Nuzhat\\Downloads\\3.jpg”, “C:\\Users\\Nuzhat\\Downloads\\2.jpg”},

            {“C:\\Users\\Nuzhat\\Downloads\\11.jpg”, “C:\\Users\\Nuzhat\\Downloads\\12.jpg”, “C:\\Users\\Nuzhat\\Downloads\\13.jpg”},

            {“C:\\Users\\Nuzhat\\Downloads\\18.jpg”, “C:\\Users\\Nuzhat\\Downloads\\19.jpg”, “C:\\Users\\Nuzhat\\Downloads\\20.jpg”}

    };



    Public GamePanel(GameFrame frame) {

        This.frame = frame;

        setLayout(new BorderLayout());

        createMainMenu();

        setupKeyBindings();

        playBackgroundMusic();

        loadSoundEffects();

    }



    Private void setupKeyBindings() {

        InputMap inputMap = getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW);

        ActionMap actionMap = getActionMap();



        String[] keys = {“UP”, “DOWN”, “LEFT”, “RIGHT”, “W”, “S”, “A”, “D”};

        For (String key : keys) {

            inputMap.put(KeyStroke.getKeyStroke(key), key);

            actionMap.put(key, new AbstractAction() {

                @Override

                Public void actionPerformed(ActionEvent e) {

                    handleKeyInput(key);

                }

            });

        }

    }



    Private void handleKeyInput(String key) {

        If (player1Panel == null || (isTwoPlayerMode && player2Panel == null)) return;



        PuzzlePanel currentPanel = isTwoPlayerMode ?

                (key.equals(“W”) || key.equals(“S”) || key.equals(“A”) || key.equals(“D”) ? player2Panel : player1Panel)

                : player1Panel;



        Boolean moved = false;

        Switch (key) {

            Case “UP”:

            Case “W”:

                Moved = currentPanel.moveTile(currentPanel.emptyRow + 1, currentPanel.emptyCol);

                Break;

            Case “DOWN”:

            Case “S”:

                Moved = currentPanel.moveTile(currentPanel.emptyRow – 1, currentPanel.emptyCol);

                Break;

            Case “LEFT”:

            Case “A”:

                Moved = currentPanel.moveTile(currentPanel.emptyRow, currentPanel.emptyCol + 1);

                Break;

            Case “RIGHT”:

            Case “D”:

                Moved = currentPanel.moveTile(currentPanel.emptyRow, currentPanel.emptyCol – 1);

                Break;

        }



        If (moved) {

            playMoveSound();

            updateMovesLabels();

            checkWinCondition();

        }

    }

