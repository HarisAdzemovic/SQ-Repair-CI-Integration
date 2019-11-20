package com.mycompany.app;
import java.util.Iterator;

public class App<T> implements Iterable<T>{
    public static void main(String[] args) {

        System.out.println("Hello World!");
    }

    public Iterator<T> iterator(){
        return new Iterator<T>() {
            Object[] elements = new Object[5];
            int i = 0;
            @Override
            public boolean hasNext() {
                return i < elements.length;
            }

            @Override
            public T next() {
                return (T) elements[i++];
            }
        };
    }
}
