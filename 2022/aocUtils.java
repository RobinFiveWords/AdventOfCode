import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.lang.Math;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Stream;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class aocUtils {

    private aocUtils() { }

    public static String readFileAsString(String fileName) throws Exception {
        String data = new String(Files.readAllBytes(Paths.get(fileName)));
        return data;
    }

    public static String[] readLinesFromFileIntoArray(String filename)
                                                     throws Exception {
        File file = new File(filename);
        Scanner sc = new Scanner(file);
        List<String> lines = new ArrayList<String>();
        while (sc.hasNextLine()) {
            lines.add(sc.nextLine().trim());
        }
        String[] arr = lines.toArray(new String[0]);
        return arr;
    }

    public static String[] bufferLinesFromFile(String filename)
                                              throws Exception {
        FileReader fr = new FileReader(filename);
        BufferedReader br = new BufferedReader(fr);
        List<String> lines = new ArrayList<String>();
        String line = null;
        while ((line = br.readLine()) != null) {
            lines.add(line);
        }
        String[] arr = lines.toArray(new String[0]);
        return arr;
    }

    public static int[] parseInts(String s) {
        List<Integer> results = new ArrayList<Integer>();
        Matcher m = Pattern.compile("\\d+").matcher(s);
        while (m.find()) {
            results.add(Integer.parseInt(m.group()));
        }
        int[] arr = results.stream().mapToInt(i->i).toArray();
        return arr;
    }

    private static int lcm2(int m, int n) {
        if (m == 0 || n == 0) return 0;
        if (n == m || n == 1) return m;
        if (m == 1) return n;
        int mm = m;
        int nn = n;
        while (mm != nn) {
            while (mm < nn) { mm += m; }
            while (nn < mm) { nn += n; }
        }
        return mm;
    }

    public static int lcm(int... ns) {
        if (ns.length == 2) return lcm2(ns[0], ns[1]);
        int result = 1;
        for (int n : ns) {
            result = lcm2(result, n);
        }
        return result;
    }

    public static void main(String[] args) {
        assert 12 == lcm(2, 3, 4);
        assert 0 == lcm(0, 1, 2);
        assert 210 == lcm(5, 6, 7);
    }
}