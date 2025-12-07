/**
 * This is the DrawingApp file which allows the user to draw different components.
 *
 * @author Aryan, Abhirath, Gathik
 * @version 1.0
 * @since 06/08/2024
 */

import javax.swing.*;
import java.awt.*;
import java.io.IOException;

/**
 * The DrawingApp class manages the frame and allows one to run the program.
 */
public class DrawingApp extends JFrame
{
    private JPanel cards;                           //CardLayout JPanel
    private Manager manager;                        //main manager
    public static final String MAIN = "Main";       //the cards that are in the cardlayout

    /**
     * Creates a Frame and initializes all the panels.
     */
    public DrawingApp() throws IOException
    {
        super("Finite State Machine Simulator");
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setSize(1500, 800);
        this.setResizable(false);

        cards = new JPanel(new CardLayout());

        manager = new ManageMainCircuit(this);
        cards.add(manager, MAIN);

        change(MAIN);

        this.getContentPane().add(cards);

        this.setVisible(true);
        this.requestFocusInWindow();
    }

    /**
     * Changes the panel to the string specified
     * @param str : the new panel
     */
    public void change(String str)
    {
        if (!str.equals(MAIN))
            throw new IllegalArgumentException(str + " is not a valid panel type.");
        ((CardLayout) (cards.getLayout())).show(cards, str);
    }

    /**
     * Returns the Manager object
     * @return the Manager object
     */
    public Manager getManager()
    {
        return manager;
    }

    public static void main(String[] args) throws IOException
    {
        new DrawingApp();
    }
}