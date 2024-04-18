import React from "react";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";

export default function PaginationSection({
  totalProducts,
  productOnPage,
  currentPage,
  setCurrentPage,
}: {
  totalProducts: number;
  productOnPage: number;
  currentPage: number;
  setCurrentPage: (page: number) => void;
}) {
  const pageNumbers = [];
  for (let i = 1; i <= Math.ceil(totalProducts / productOnPage); i++) {
    pageNumbers.push(i);
  }

  const maxPageNum = 3;
  const pageNumLimit = Math.floor(maxPageNum / 2);

  let activePages = pageNumbers.slice(
    Math.max(1, currentPage - 1 - pageNumLimit),
    Math.min(currentPage - 1 + pageNumLimit + 1, pageNumbers.length - 1)
  );

  activePages.unshift(1);
  activePages.push(pageNumbers.length);

  const handleNextPage = () => {
    if (currentPage < pageNumbers.length) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const renderPages = () => {
    const renderedPages = activePages.map((page, idx) => (
      <PaginationItem
        key={idx}
        className={currentPage === page ? "bg-primary rounded-md" : ""}
      >
        <PaginationLink onClick={() => setCurrentPage(page)}>
          {page}
        </PaginationLink>
      </PaginationItem>
    ));

    if (activePages[1] > 2) {
      renderedPages.splice(1, 0, <PaginationEllipsis key="ellipsis-start" />);
    }

    if (activePages[activePages.length - 2] < pageNumbers.length - 1) {
      renderedPages.splice(
        renderedPages.length - 1,
        0,
        <PaginationEllipsis key="ellipsis-end" />
      );
    }

    console.log("renderedPages", renderedPages);

    return renderedPages;
  };

  return (
    <Pagination>
      <PaginationContent>
        <PaginationItem>
          <PaginationPrevious
            onClick={handlePrevPage}
            aria-disabled={currentPage <= 1}
            tabIndex={currentPage <= 1 ? -1 : undefined}
            className={
              currentPage <= 1 ? "pointer-events-none opacity-50" : undefined
            }
          />
        </PaginationItem>

        {renderPages()}

        <PaginationItem>
          <PaginationNext
            onClick={handleNextPage}
            aria-disabled={currentPage == pageNumbers.length}
            tabIndex={currentPage == pageNumbers.length ? -1 : undefined}
            className={
              currentPage == pageNumbers.length
                ? "pointer-events-none opacity-50"
                : undefined
            }
          />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  );
}
