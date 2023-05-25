import { ReactElement, useContext } from "react";
import { BorrowedIn } from "../CustomTypes";
import { Link } from "react-router-dom";
import LibrarianLinks from "./LibrarianLinks";
import { AuthContext } from "../contexts/AuthContext";

interface BorrowedListProps {
  borrowedList: BorrowedIn[];
}

export function BorrowedList(props: BorrowedListProps): ReactElement {
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);
  return (
    <ul>
      {props.borrowedList.map((borrowed: BorrowedIn, index: number) => (
        <li>
          <h3>{borrowed.copy.book.title}</h3>
          <p>Issue Date: {borrowed.issueDate.split("T").join(" ")}</p>
          <p>Due Date: {borrowed.dueDate.split("T").join(" ")}</p>
          <p>Return Date: {borrowed.returnDate?.split("T").join(" ")}</p>
          {!borrowed.returnDate && (
            <Link to={`/borrowed/${borrowed.id}/return`}>Return</Link>
          )}
          {isLibrarian && <LibrarianLinks url={`/borrowed/${borrowed.id}`} />}
        </li>
      ))}
    </ul>
  );
}
