import java.io.FileWriter;
import java.io.File;

public class LogGenerator
{
    public static void main(final String[] array) throws Exception
    {
        int i = 1;
        final File file = new File("/tmp/ServerLogs");
        if (!file.exists())
        {
            if (file.mkdir())
            {
                System.out.println("ServerLogs Directory created!");
                while (i <= 100)
                {
                  final File file2 = new File("/tmp/ServerLogs/" + i);
                  if (file2.createNewFile())
                  {
                    final FileWriter fileWriter = new FileWriter(file2);
                    while (file2.length() < 10240L)
                    {
                        fileWriter.write("Connection to the server started..." + i + "\n");
                        fileWriter.write("Server connected at port 97654..." + i + "\n");
                        fileWriter.write("Data logged for file " + i + "\n");
                        fileWriter.write("Server disconnected..." + i + "\n");
                        fileWriter.write("Connection stopped..." + i + "\n");
                    }
                    fileWriter.close();
                    System.out.println("File is created!");
                    ++i;
                 }
                 else
                 {
                    System.out.println("File not created!");
                 }
               }
            }
            else
            {
                System.out.println("Unable to create ServerLogs Directory!");
            }
        }
        else
        {
            System.out.println("ServerLogs Directory already exists!");
        }
    }//end main
}
